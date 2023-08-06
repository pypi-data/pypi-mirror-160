"""Publish properties (configs) from github to google drive
"""

import os

from compipe.exception.general_warning import WarningGotEmptyValue
from compipe.exception.validate_error import GErrorKeyNotFound
from compipe.response.command_result import MSGStatusCodes
from compipe.utils.io_helper import json_loader
from compipe.utils.logging import logger
from compipe.utils.parameters import ARG_OBJ, ARG_OUTPUT, ARG_DATA
from compipe.utils.singleton import Singleton
from compipe.utils.task_queue_helper import TQHelper
from typing import Dict

from .resolver.asset_resolver import AssetResolver, ResolverParam
from .resolver.resolver_parameter import ResolverParam

"""

Below config is to declare the properties repos.
It could help tars service to address the incoming webhook event
The incoming webhook URL should be ending with one of the key name of below declarations

ignore_path: it would skip building the configs when matching to the ignore lists.

"""

# collect the full lists of model names, it would be used to
# verify the class name parameter
# /////////////////////////////////////////////////////////////////////


class AssetPopulator(metaclass=Singleton):

    def __init__(self, resolver_cfg_path: str):
        self.resolver_cfg_path = resolver_cfg_path
        self.resolver_cfg_data = json_loader(self.resolver_cfg_path)
        self.resolvers = {key: ResolverParam.parse_obj(value) for key, value in self.resolver_cfg_data.items()}

    def get_resolver_param(self, model_name: str) -> ResolverParam:
        if not (resolver_param_data := self.resolver_cfg_data.get(model_name, None)):
            raise GErrorKeyNotFound(f'Not found model: {model_name}')

        return ResolverParam.parse_obj(resolver_param_data)

    def get_resolver(self, model_name: str):
        self.get_resolver_param(model_name=model_name)

    def clean_up_temporary_keys(self, data: Dict):

        # tmp attribute name has '_' prefix
        _tmp_keys = [key for key in data.keys() if key[0] == '_']

        # remove keys
        for _key in _tmp_keys:
            # remove temporary key from the data config
            del data[_key]

        return data

    def populate(self, resolver: AssetResolver, filters: list):
        """Generate the published configs to github.

        Arguments:
            filters {list} -- Represent the config lists.

        Returns:
            [list] -- Represent the populated config lists, '[]' empty lists
            means 
        """

        # keep all the influenced configs that will be exported later
        # //////////////////////////////////////////////////////////////////
        cfg_stacks = set()

        if not filters:
            # build all configs on the specific resolver
            # //////////////////////////////////////////////////////////////
            cfg_stacks.update([item for sublist in resolver.dependency.values() for item in sublist])
        else:
            # only build the selected configs of the resolver
            # //////////////////////////////////////////////////////////////
            for cfg in filters:
                for _, configs in resolver.dependency.items():

                    # the filter item is represented by the config basename,
                    # we would need to re-format the lists before compareing
                    # //////////////////////////////////////////////////////
                    shorten_cfg_lists = [os.path.split(cfg)[-1] for cfg in configs]
                    if cfg in shorten_cfg_lists:
                        index = shorten_cfg_lists.index(cfg)
                        cfg_stacks.update(configs[index:])

        if not cfg_stacks:
            raise WarningGotEmptyValue('No config need to be resolved!')

        for path, config in resolver.configs.items():
            if path in cfg_stacks:
                logger.debug(f'Populate object: [{path}]')
                asset = config.get(ARG_OBJ)

                if asset and asset.publish > 0:
                    # if the file does exist, it would load the sha hash value for
                    # perform 'update' instead of 'add' on git.
                    # /////////////////////////////////////////////////////////////////////
                    sha = resolver.repo_helper.export_files.get(config[ARG_OUTPUT])

                    # clean up data before committing
                    config_data = self.clean_up_temporary_keys(data=config[ARG_DATA])

                    # commit the changes to git repo
                    # /////////////////////////////////////////////////////////////////////
                    (is_uploaded, msg) = resolver.repo_helper.commit(output=config[ARG_OUTPUT],
                                                                     data=config_data,
                                                                     sha=sha,
                                                                     branch=resolver.main_branch)

                    TQHelper.post(payload=msg,
                                  msg_status=MSGStatusCodes.success if is_uploaded else MSGStatusCodes.warning)

                else:
                    # ignore unpublished asset
                    # /////////////////////////////////////////////////////////////////////
                    TQHelper.post(payload=f'Skipped unpublished config: {path}',
                                  msg_status=MSGStatusCodes.warning)

        return 'Done'
