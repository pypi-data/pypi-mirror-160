from pydantic import BaseModel, Field, validator

SUPPORT_RESOLUTION = [2048, 1280, 1024, 512, 256, 128, 64, 32, 16]


class Resolution(BaseModel):
    width: int = Field(1024,
                       title='Image Width')

    height: int = Field(1024,
                        title='Image Height')

    @validator('width', 'height')
    def is_valid_resolution_values(cls, v):  # pylint: disable=no-self-argument
        if not v in SUPPORT_RESOLUTION:
            raise ValueError('resolution must be one of the value from '
                             f'the lists \n[{"/".join(SUPPORT_RESOLUTION)}]')
        # if not math.log(v, 2).is_integer():
        #     raise ValueError('must be a power of two value.')
        return v

    @property
    def values(self):
        return (self.width, self.height)
