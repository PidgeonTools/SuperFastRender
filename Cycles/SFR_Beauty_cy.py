import bpy
from bpy.types import (
    Operator
)


class SFR_Beauty_cy(Operator):
    bl_idname = "render.superfastrender_b"
    bl_label = "Beauty"
    bl_description = "Optimizes the scene for beauty rendering, this is a general optimization step"

    def execute(self, context):
        scene = bpy.context.scene
        cycles = scene.cycles

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        scene.render.use_persistent_data = True

        # set adaptive samples
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.005
        cycles.adaptive_min_samples = 64

        # set max bounces
        cycles.max_bounces = 1024
        cycles.diffuse_bounces = 1024
        cycles.glossy_bounces = 1024
        cycles.transparent_max_bounces = 1024
        cycles.transmission_bounces = 1024
        cycles.volume_bounces = 1024

        # set clamps to reduce fireflies
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 0

        # set caustic settings
        cycles.caustics_reflective = True
        cycles.caustics_refractive = True
        cycles.blur_glossy = 0

        # change volume settings
        cycles.volume_step_rate = 1
        cycles.volume_preview_step_rate = 1
        cycles.volume_max_steps = 1024

        # simplfy the scene
        scene.render.use_simplify = False
        # culling
        cycles.use_camera_cull = False
        cycles.use_distance_cull = False

        self.report({'INFO'}, "Beauty preset applied for Cycles")

        return {'FINISHED'}
