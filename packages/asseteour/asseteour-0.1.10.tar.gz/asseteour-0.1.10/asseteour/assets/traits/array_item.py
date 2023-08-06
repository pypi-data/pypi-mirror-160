
from pydantic import BaseModel, Field


class BaseArrayItem(BaseModel):

    name: str = Field(...,
                      title='Item identity',
                      description='Represent the unique item key name')

    is_enabled: bool = Field(True,
                             title='Enable flag',
                             description='Represent the available states.')
