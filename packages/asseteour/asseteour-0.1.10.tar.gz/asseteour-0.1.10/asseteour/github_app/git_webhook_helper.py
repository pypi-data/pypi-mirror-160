import hashlib
import hmac
import json
import os
import pickle
import re
import shlex
from collections import defaultdict

from compipe.cmd_wrapper import create_command_payload
from compipe.utils.decorators import (required_params,
                                      verify_webhook_secret_sha1)
from compipe.utils.decorators_exception_handler import exception_handler
from compipe.utils.parameters import ARG_CLASS, ARG_PAYLOAD, ARG_POPULATE


class Generic:
    """Resolve the json string into a generic class instance
    It could allow to use class property syntax to access the key/value from dict.
    """
    @classmethod
    def from_dict(cls, dict):
        obj = cls()
        obj.__dict__.update(dict)
        return obj


@verify_webhook_secret_sha1(header='sha1=')
@required_params(ARG_PAYLOAD)
@exception_handler
def github_properties_populate(*args, **kwargs):
    """Populate the property configs from the github webhook payload.
    [TODO] Implement the function to address 'remove' action.
    """

    payload = kwargs.get(ARG_PAYLOAD).json
    payload = json.loads(json.dumps(payload), object_hook=Generic.from_dict)
    configs = []
    for commit in payload.commits:
        # only populate the configs attaching 'populate' in the commit message
        if commit.message.startswith('populate'):
            configs += commit.modified
            configs += commit.added

    # sort out config in dict
    config_mapping = defaultdict(list)
    for cfg in configs:
        matched = re.search(r'^Data/(\w+)/.+', cfg)
        if matched:
            config_mapping[matched[1]].append(os.path.basename(os.path.splitext(cfg)[0]))

    # only update when having valid configs to be updated
    for key, value in config_mapping.items():
        cmd_payload = {
            'user': 'U014SE6JH7Y',
            'command': ' '.join([ARG_POPULATE, f'{ARG_CLASS}={key}', *value]),
            'channel': 'T015BP2HUU9#C015DF11US0',
            'response': 'SlackChannel'
        }

        create_command_payload(args=cmd_payload)
