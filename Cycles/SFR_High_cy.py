import bpy
from bpy.types import (
    Operator
)


class SFR_High_cy(Operator):
    bl_idname = "render.superfastrender_h"
    bl_label = "High"
    bl_description = "Optimizes the scene for fast rendering, this is a general optimization step"

    def execute(self, context):
        scene = bpy.context.scene
        cycles = scene.cycles

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        scene.render.use_persistent_data = True

        # set adaptive samples
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.01
        cycles.adaptive_min_samples = 64

        # set max bounces
        cycles.max_bounces = 16
        cycles.diffuse_bounces = 2
        cycles.glossy_bounces = 4
        cycles.transparent_max_bounces = 8
        cycles.transmission_bounces = 2
        cycles.volume_bounces = 0

        # set clamps to reduce fireflies
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 10

        # set caustic settings
        cycles.caustics_reflective = False
        cycles.caustics_refractive = False
        cycles.blur_glossy = 0.5

        # change volume settings
        cycles.volume_step_rate = 2.5
        cycles.volume_preview_step_rate = 2.5
        cycles.volume_max_steps = 512

        # simplfy the scene
        scene.render.use_simplify = True
        # viewport
        scene.render.simplify_subdivision = 2
        scene.render.simplify_child_particles = 0.5
        cycles.texture_limit = '2048'
        cycles.ao_bounces = 4
        # render
        scene.render.simplify_subdivision_render = 5
        scene.render.simplify_child_particles_render = 1
        cycles.texture_limit_render = '8192'
        cycles.ao_bounces_render = 5
        # culling
        cycles.use_camera_cull = True
        cycles.use_distance_cull = True
        cycles.camera_cull_margin = 0.01
        cycles.distance_cull_margin = 100

        self.report({'INFO'}, "High preset applied for Cycles")

        return {'FINISHED'}
