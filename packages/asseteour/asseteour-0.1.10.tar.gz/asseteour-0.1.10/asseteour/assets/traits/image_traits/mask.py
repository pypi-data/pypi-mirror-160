from typing import List

from pydantic import BaseModel, Field

from ..values import ClipRangeInt
from .image import Resolution


class Mask(BaseModel):
    source: str = Field('',
                        title='Mask file',
                        description='Represent the local path of the mask file')

    output: str = Field('',
                        title='Output file path',
                        description='Represent mask file guid on google drive')

    border: int = Field(40,
                        title='Mask Border width',
                        description='border could help get better result when '
                        'meeting the situation of cutting mask on image edges',
                        ge=0)

    reverse: bool = Field(True,
                          title='Reverse mask',
                          description='Reverse the float value of the grayscale '
                          'mask. (e.g. 1.0 - 0.2 = 0.8)')

    reverse_bias: int = Field(1,
                              title='Bias value to reverse',
                              description='The new grayscale value would be the '
                              'Subtraction of bias and orgin value',
                              ge=1)


    resolution: Resolution = Field(Resolution(width=1024, height=1024),
                                   title='Mask Resolution',
                                   description='Represent the new resolution of mask image')

    clip_range: ClipRangeInt = Field(ClipRangeInt(start=0, end=100),
                                     title='Shadow Shape Scale',
                                     description='Represent the scale value to generate'
                                     'the shadow from DC texture. 0: means no shadow')

    class Config:

        # extra ： https://pydantic-docs.helpmanual.io/usage/model_config
        # 'ignore' will silently ignore any extra attributes,
        # 'allow' will assign the attributes to the model.
        extra = 'allow'
