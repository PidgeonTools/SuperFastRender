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

#### SETTINGS OPTIMIZER ####

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
        default=50,
        max=100,
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

#### TEXTURE OPTIMIZER ####

    diffuse_resize: IntProperty(
        name="Diffuse / Albedo",
        default=0,
        max=7,
        min=0,
        description="the factor by which the diffuse or albedo textures will be scaled down, 0 = unaffected \nrecommended: 0",
        options=set(),  # Not animatable!
    )
    ao_resize: IntProperty(
        name="Ambient Occlusion",
        default=2,
        max=7,
        min=0,
        description="the factor by which the ambient occlusion textures will be scaled down, 0 = unaffected \nrecommended: 2",
        options=set(),  # Not animatable!
    )
    specular_resize: IntProperty(
        name="Specular / Metallic",
        default=2,
        max=7,
        min=0,
        description="the factor by which the specular or metallic textures will be scaled down, 0 = unaffected \nrecommended: 2",
        options=set(),  # Not animatable!
    )
    roughness_resize: IntProperty(
        name="Roughness / Glossiness",
        default=2,
        max=7,
        min=0,
        description="the factor by which the roughness or glossiness textures will be scaled down, 0 = unaffected \nrecommended: 2",
        options=set(),  # Not animatable!
    )
    normal_resize: IntProperty(
        name="Normal / Bump",
        default=1,
        max=7,
        min=0,
        description="the factor by which the normal or bump textures will be scaled down, 0 = unaffected \nrecommended: 1",
        options=set(),  # Not animatable!
    )
    opacity_resize: IntProperty(
        name="Opacity / Transparency",
        default=1,
        max=7,
        min=0,
        description="the factor by which the opacity or transparency textures will be scaled down, 0 = unaffected \nrecommended: 1",
        options=set(),  # Not animatable!
    )
    translucency_resize: IntProperty(
        name="Translucency",
        default=1,
        max=7,
        min=0,
        description="the factor by which the translucency textures will be scaled down, 0 = unaffected \nrecommended: 1",
        options=set(),  # Not animatable!
    )
    create_backup: BoolProperty(
        name="Create Backup",
        default=True,
        description='Creates a backup of all the image files in the folder "textures backup"\nwe heavily recommend to keep this enabled'
    )

#### MESH OPTIMIZER ####

    mo_max_quality: FloatProperty(
        name="max. Quality",
        default=1,
        max=1,
        min=0.5,
        description="values below 1 means that it will never be at full qualtiy\nrecommended: 1",
        options=set(),  # Not animatable!
    )

    mo_min_quality: FloatProperty(
        name="min. Quality",
        default=0.05,
        max=0.5,
        min=0,
        description="values above 0 will limit how much the mesh will be optimized\nrecommended: 0.05",
        options=set(),  # Not animatable!
    )

    mo_quality_change: FloatProperty(
        name="Quality change",
        default=0.1,
        max=1.0,
        min=0.01,
        description="how quickly your mesh quality should be reduced in relation to distance\nrecommended: 0.1",
        options=set(),  # Not animatable!
    )

    mo_frame_skipped: IntProperty(
        name="Frame Offset",
        default=50,
        max=100,
        min=1,
        description="Frames between mesh optimization steps",
        options=set(),  # Not animatable!
    )