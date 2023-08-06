"""Populate the property objects
"""

import typing
from typing import List

from pydantic import BaseModel, Field

from .base_asset_wrapper import BaseAssetWrapper


class SchemaRepo(BaseModel):

    repo: str = Field('',
                      title='git repo name',
                      description='represent the repo full path.')

    path: str = Field('',
                      title='the repo path of the schema file',
                      description='represent the resolver name.')

    main_branch: str = Field('',
                             title='main branch name',
                             description='represent the resolver name.')


class ResolverParam(BaseModel):
    #
    filter_source: str = Field('',
                               title='Source filter (regex)',
                               description='represent the source filter pattern for looking for the matched configs')

    filter_export: str = Field('',
                               title='export filter (regex)',
                               description='represent the export fitler pattern which would be used to check if the config'
                               'is an "add" commit. The repo helper would perform "add" behavior instead of "update"')

    output_path: str = Field('',
                             title='Output path',
                             description='the target path for storing the full payload configs.')

    ignore_paths: List[str] = Field([],
                                    title='Ignore path list',
                                    description='represent the paths for excluding the configs when populating full payload data')

    repo: str = Field('',
                      title='git repo name',
                      description='represent the repo full path.')

    base_url: str = Field('',
                          title='Github Enterprise with custom hostname')

    name: str = Field('',
                      title='resolver name',
                      description='represent the resolver name.')

    main_branch: str = Field('',
                             title='main branch name',
                             description='represent the resolver name.')

    model_name: str = Field('',
                            title='model class name',
                            description='represent the pydantic model class name.')

    model: typing.Type[BaseAssetWrapper] = Field(None,
                                                 title='model object',
                                                 description='represent the pydantic model object.')

    resolver: typing.Any = Field(None,
                                 title='resolver object',
                                 description='represent the pydantic resolver object.')

    model_schema: SchemaRepo = Field(None,
                                     title='schema git repo definition',
                                     description='Represent the git repo information which would '
                                     'be used to export the schema file.')
