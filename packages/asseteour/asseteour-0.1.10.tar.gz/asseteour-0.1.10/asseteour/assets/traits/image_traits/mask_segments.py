from enum import Enum
from pydantic import Field
from ..array_item import BaseArrayItem


class GSize(str, Enum):
    xxxs = 'xxx_small'
    xxs = 'xx_small'
    xs = 'x_small'
    s = 'small'
    m = 'medium'
    l = 'large'
    xl = 'x_large'
    xxl = 'xx_large'
    xxxl = 'xxx_large'


class PickRule(int, Enum):
    random = 1
    consequent = 2


class Segment(BaseArrayItem):
    value: float = Field(0.05,
                         title='Grayscale Value',
                         description='Represent the value of '
                         'contour level. Range (0.0 ~ 1.0',
                         ge=0.05,
                         le=1.0
                         )

    number: int = Field(5,
                        title='Point numbers',
                        description='Represent the point numbers '
                        'to be generated in the valid contour area.',
                        ge=0
                        )

    radius: int = Field(1,
                        title='Point numbers',
                        description='Represent the point numbers '
                        'to be generated in the valid contour area.',
                        ge=1
                        )

    timeout: int = Field(10,
                         title='Timeout',
                         description='Represent the timeout when '
                         'generating points. The process could be '
                         'forced stop when encounter timeout')

    shadow_scale: float = Field(0,
                                title='Shadow Shape Scale',
                                description='Represent the scale value to generate'
                                'the shadow from DC texture. 0: means no shadow',
                                ge=0,
                                le=1)

    resource: str = Field(...,
                          title='Resource folder ID',
                          description='Represent the folder ID of the '
                          'segment resources on google drive')

    pick_rule: PickRule = Field(PickRule.random,
                                title='Resource picking rule',
                                description='Represent the rule of selecting assets from resource. '
                                '1: select asset randomly from the specific folder.'
                                '2: loop asset consequently from the specific folder.')

    class Config:
        schema_extra = {
            'examples': [{
                'name': GSize.s,
                'enable': True,
                'value': 0.08,
                'timeout': 10,
                'number': 10,
                'radius': 10,
                'resource': '1AAozk1mJOVuY7h5zbDXAzpSx749E9E68'
            }]
        }
