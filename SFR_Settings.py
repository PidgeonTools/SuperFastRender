import bpy

from bpy.types import (
    PropertyGroup,
)
from bpy.props import (
    EnumProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    BoolProperty
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
        default='AUTOMATIC',
        description="Optimization method, manual for basic setups, automatic for more precise settings",
        options=set(),  # Not animatable!
    )
    threshold: FloatProperty(
        name="Threshold",
        default=0.1,
        max=1,
        min=0.01,
        description="Threshold on which the next benchmark method should set in",
        options=set(),  # Not animatable!
    )
    resolution: IntProperty(
        name="Benchmark Res",
        default=5,
        max=20,
        min=1,
        description="Resolution the benchmark should run, higher = more precision but slower",
        options=set(),  # Not animatable!
    )
    frame_skipped: IntProperty(
        name="Frame Offset",
        default=10,
        max=20,
        min=1,
        description="Frames between automatic benchmarks",
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
    use_diffuse: BoolProperty(
        name="Diffuse",
        default=True,
        description="Benchmark diffuse"
    )
    use_glossy: BoolProperty(
        name="Glossy",
        default=True,
        description="Benchmark glossy"
    )
    use_transparent: BoolProperty(
        name="Transparency",
        default=True,
        description="Benchmark transparency"
    )
    use_transmission: BoolProperty(
        name="Transmission",
        default=True,
        description="Benchmark transmission"
    )
    use_volume: BoolProperty(
        name="Volume",
        default=True,
        description="Benchmark volume"
    )
    use_indirect: BoolProperty(
        name="Indirect Brightness",
        default=True,
        description="Benchmark indirect brightness"
    )
    use_caustics: BoolProperty(
        name="Caustics",
        default=False,
        description="Benchmark caustic blur"
    )
