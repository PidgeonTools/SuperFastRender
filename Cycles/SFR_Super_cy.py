import bpy
from bpy.types import (
    Operator
)


class SFR_Super_cy(Operator):
    bl_idname = "render.superfastrender_s"
    bl_label = "SUPER"
    bl_description = "Optimizes the scene for fastest rendering, this is a general optimization step"

    def execute(self, context):
        prefs = bpy.context.preferences.addons['cycles'].preferences
        scene = bpy.context.scene
        cycles = scene.cycles

        for device_type in prefs.get_device_types(bpy.context):
            prefs.get_devices_for_type(device_type[0])

        if prefs.get_devices_for_type == 'OPTIX':
            scene.render.tile_x = 200
            scene.render.tile_y = 200
        elif prefs.get_devices_for_type == 'CUDA':
            scene.render.tile_x = 200
            scene.render.tile_y = 200
        elif prefs.get_devices_for_type == 'OPENCL':
            scene.render.tile_x = 200
            scene.render.tile_y = 200
        elif prefs.get_devices_for_type == 'CPU':
            scene.render.tile_x = 32
            scene.render.tile_y = 32

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        scene.render.use_persistent_data = True
        #scene.render.use_save_buffers = True

        # set adaptive samples
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.05
        cycles.adaptive_min_samples = 8

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
        cycles.volume_step_rate = 5
        cycles.volume_preview_step_rate = 5
        cycles.volume_max_steps = 256

        # simplfy the scene
        scene.render.use_simplify = True
        # viewport
        scene.render.simplify_subdivision = 2
        scene.render.simplify_child_particles = 0.2
        cycles.texture_limit = '2048'
        cycles.ao_bounces = 2
        # render
        scene.render.simplify_subdivision_render = 4
        scene.render.simplify_child_particles_render = 1
        cycles.texture_limit_render = '4096'
        cycles.ao_bounces_render = 4
        # culling
        cycles.use_camera_cull = True
        cycles.use_distance_cull = True
        cycles.camera_cull_margin = 0.1
        cycles.distance_cull_margin = 50

        self.report({'INFO'}, "SUPER preset applied for Cycles")

        return {'FINISHED'}
