import bpy

from bpy.types import (
    PropertyGroup,
)
from bpy.props import (
    EnumProperty,
    IntProperty,
    FloatProperty,
    StringProperty
)


class SFR_Settings(PropertyGroup):

    detection_method: EnumProperty(
        name="Optimization Method",
        items=(
            (
                'MANUAL',
                'Manual',
                'Manual Scene Optimizer'
            ),
            (
                'AUTOMATIC',
                'Automatic',
                'Automatic Scene Optimizer'
            ),
        ),
        default='MANUAL',
        description="Choose the optimization method, manual for basic setups, automatic for more precise settings",
        options=set(),  # Not animatable!
    )
    threshold: FloatProperty(
        name="Threshold",
        default=1,
        max=100,
        min=0.001,
        description="Choose the threshold on which the next benchmark method should set in",
        options=set(),  # Not animatable!
    )
    resolution: IntProperty(
        name="Benchmark Res",
        default=5,
        max=100,
        min=1,
        description="Choose the resolution the Benchmark should run, higher = more precision but slower",
        options=set(),  # Not animatable!
    )
    inputdir: StringProperty(
        name="Benchmark Folder",
        default="C:/temp/",
        description="Benchmarking Frames will be saved here",
        subtype='DIR_PATH',
        maxlen=1024,
        options=set(),  # Not animatable!
    )
