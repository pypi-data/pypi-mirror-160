import json
import re
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, validator, Extra


class Metadata(BaseModel, extra=Extra.forbid):
    guid: str = Field(
        "",
        title='Config GUID',
        description='Represent the GUID value'
    )

    publish: int = Field(
        1,
        title='Publishing state',
        description='Represent the index value of the publishing state.'
        'There are four different state level to control the config visiblity '
        'for different dev route: \n'
        '0-> Not publish (e.g. config tempalte)\n'
        '1-> Publish to the internel developing stage\n'
        '2-> Publish to the BETA testing stage\n'
        '3 ~ 9 -> Placeholders for the new requirements of other stages\n'
        '10-> Publish to the Live game',
        ge=0,
        le=10
    )

    parent: Optional[str] = Field(
        '',
        title='Config Parent Path',
        description='Represent the parent path, '
        'it would be used to perform a full copy of '
        'the object payload. Some of the settings are '
        'inherited from parent, the reset of settings are '
        'overrided by itself.'
    )

    tags: Optional[List[str]] = Field(
        [],
        title='Object Tags Information',
        description='Represent the object categories',
        min_items=1
    )

    name: Optional[str] = Field(
        '',
        title='Object Name',
        description="It would be updated to the config file name automatically."
        "It's a read-only property."
    )

    @validator('guid')
    def guid_is_not_empty(cls, v):  # pylint: disable=no-self-argument
        if not v:
            raise ValueError('must contain a valid guid')
        return v

    @validator('parent')
    def parent_path_start_with_root(cls, v):  # pylint: disable=no-self-argument
        if v:
            if not v.startswith('Data'):
                raise ValueError('Invalid path: must starts with "Data" root path')
            if re.fullmatch(r'.*\.\w+', v):
                raise ValueError('Invalid path: can\'t contain file extension')
        return v
