from pydantic import BaseModel, Field


class ClipRangeInt(BaseModel):
    """[Deprecated: use 'Threshold' to replace] Represent the threshold 
    Values (Region of interest).

    """
    start: int = Field(...,
                       title='The lower threshold of Clip Range',
                       ge=0,
                       le=10000)
    end: int = Field(...,
                     title='The upper threshold of Clip Range',
                     ge=0,
                     le=10000)

    class Config:
        schema_extra = {
            'examples': [
                {
                    'start': 0,
                    'end': 100
                }
            ]
        }


class ThresholdUnsignedRange(BaseModel):
    """Represent the threshold range values (Region of interest)

    """
    min: int = Field(...,
                     title='The lower threshold of the Range',
                     ge=0,
                     le=10000)
    max: int = Field(...,
                     title='The upper threshold of the Range',
                     ge=0,
                     le=10000)

    @property
    def values(self):
        return (self.min, self.max)

    @property
    def is_valid(self):
        return self.max > self.min

    class Config:
        schema_extra = {
            'examples': [
                {
                    'min': 0,
                    'max': 3000
                }
            ]
        }


class ThresholdRange(BaseModel):
    """Represent the threshold range values (Region of interest)

    """
    min: int = Field(...,
                     title='The lower threshold of the Range',
                     ge=-10000,
                     le=10000)
    max: int = Field(...,
                     title='The upper threshold of the Range',
                     ge=-10000,
                     le=10000)

    @property
    def values(self):
        return (self.min, self.max)

    @property
    def is_valid(self):
        return self.max > self.min

    def set_values(self, range=(0, 0)):
        self.min = range[0]
        self.max = range[1]

    class Config:
        schema_extra = {
            'examples': [
                {
                    'min': 0,
                    'max': 3000
                }
            ]
        }


class VolumeFloatRange(BaseModel):
    """Represent the volume range values (Unit: M3)

    """
    min: float = Field(...,
                       title='The lower threshold of the Range',
                       ge=0,
                       le=1)
    max: float = Field(...,
                       title='The upper threshold of the Range',
                       ge=0,
                       le=1)

    @property
    def values(self):
        return (self.min, self.max)

    @property
    def is_valid(self):
        return self.max > self.min

    def set_values(self, range=(0, 0)):
        self.min = range[0]
        self.max = range[1]

    class Config:
        schema_extra = {
            'examples': [
                {
                    'min': 0.0001,
                    'max': 1
                }
            ]
        }


class ThresholdRange3D(BaseModel):
    """Represent the threshold range values (Region of interest)

    Use cases:
        Medical Dicom: Define the borders of clipping 3d volume data (dicom dataset)
           width: Represent the width of axial plane.
           height: Represent the height of axial plane.
           depth: Represent the height of coronal/sagittal plane.
           offset_x: Represent the border offset value along axial plane.
           offset_y: Represent the border offset value along axial plane.
           offset_z: Represent the border offset value along coronal/sagittal plane

    """
    width: int = Field(...,
                       title='Represent the width along the X-Axis',
                       ge=0,
                       le=2000)
    height: int = Field(...,
                        title='Represent the height along the Y-Axis',
                        ge=0,
                        le=2000)

    depth: int = Field(...,
                       title='Represent the depth along the Z-Axis',
                       ge=0,
                       le=2000)

    offset_x: int = Field(...,
                          title='Represent the border offset value along X-Axis',
                          ge=0,
                          le=2000)
    offset_y: int = Field(...,
                          title='Represent the border offset value along Y-Axis',
                          ge=0,
                          le=2000)

    offset_z: int = Field(...,
                          title='Represent the border offset value along Z-Axis',
                          ge=0,
                          le=2000)

    class Config:
        schema_extra = {
            'examples': [
                {
                    'width': 0,
                    'height': 0,
                    'depth': 0,
                    'offset_x': 0,
                    'offset_y': 0,
                    'offset_z': 0
                }
            ]
        }

    @property
    def is_valid(self):
        return (self.width and self.height and self.depth)

    @property
    def values(self):
        return ((self.width, self.height, self.depth),
                (self.offset_x, self.offset_y, self.offset_z))

    def __repr__(self):
        return str(self.values)
