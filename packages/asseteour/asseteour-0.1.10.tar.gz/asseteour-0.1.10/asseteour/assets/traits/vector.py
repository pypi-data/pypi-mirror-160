from pydantic import BaseModel, Field


class vectorFloat3d(BaseModel):
    x: float = Field(0,
                     title='X - Axis')

    y: float = Field(0,
                     title='Y - Axis')

    z: float = Field(0,
                     title='Z - Axis')

    @property
    def values(self):
        return (self.x, self.y, self.z)

    @property
    def IsZero(self):
        return self.x + self.y + self.z == 0

    class Config:
        schema_extra = {
            'examples': [
                {
                    'x': 2,
                    'y': 0,
                    'z': 1
                }
            ]
        }


class vectorInt3d(BaseModel):
    x: int = Field(0,
                   title='X - Axis')

    y: int = Field(0,
                   title='Y - Axis')

    z: int = Field(0,
                   title='Z - Axis')

    @property
    def is_valid(self):
        return any(self.values)

    @property
    def values(self):
        return (self.x, self.y, self.z)

    class Config:
        schema_extra = {
            'examples': [
                {
                    'x': 2,
                    'y': 0,
                    'z': 1
                }
            ]
        }
