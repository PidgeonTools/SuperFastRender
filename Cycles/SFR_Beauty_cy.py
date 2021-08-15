import bpy
from bpy.types import (
    Operator
)


class SFR_Beauty_cy(Operator):
    bl_idname = "render.superfastrender_b"
    bl_label = "Beauty"
    bl_description = "Optimizes the scene for beauty rendering, this is a general optimization step"

    def execute(self, context):
        prefs = bpy.context.preferences.addons['cycles'].preferences

        for device_type in prefs.get_device_types(bpy.context):
            prefs.get_devices_for_type(device_type[0])

        if prefs.get_devices_for_type == 'OPTIX':
            bpy.context.scene.render.tile_x = 200
            bpy.context.scene.render.tile_y = 200
        elif prefs.get_devices_for_type == 'CUDA':
            bpy.context.scene.render.tile_x = 200
            bpy.context.scene.render.tile_y = 200
        elif prefs.get_devices_for_type == 'OPENCL':
            bpy.context.scene.render.tile_x = 200
            bpy.context.scene.render.tile_y = 200
        elif prefs.get_devices_for_type == 'CPU':
            bpy.context.scene.render.tile_x = 32
            bpy.context.scene.render.tile_y = 32

        bpy.context.scene.cycles.debug_use_spatial_splits = True
        bpy.context.scene.cycles.debug_use_hair_bvh = True
        bpy.context.scene.render.use_persistent_data = True
        bpy.context.scene.render.use_save_buffers = True

        # set adaptive samples
        bpy.context.scene.cycles.use_adaptive_sampling = True
        bpy.context.scene.cycles.adaptive_threshold = 0.001
        bpy.context.scene.cycles.adaptive_min_samples = 64

        # set max bounces
        bpy.context.scene.cycles.max_bounces = 24
        bpy.context.scene.cycles.diffuse_bounces = 24
        bpy.context.scene.cycles.glossy_bounces = 24
        bpy.context.scene.cycles.transparent_max_bounces = 24
        bpy.context.scene.cycles.transmission_bounces = 24
        bpy.context.scene.cycles.volume_bounces = 2

        # set clamps to reduce fireflies
        bpy.context.scene.cycles.sample_clamp_direct = 0
        bpy.context.scene.cycles.sample_clamp_indirect = 50

        # set caustic settings
        bpy.context.scene.cycles.caustics_reflective = False
        bpy.context.scene.cycles.caustics_refractive = False
        bpy.context.scene.cycles.blur_glossy = 0.1

        # change volume settings
        bpy.context.scene.cycles.volume_step_rate = 1
        bpy.context.scene.cycles.volume_preview_step_rate = 1
        bpy.context.scene.cycles.volume_max_steps = 1024

        # simplfy the scene
        bpy.context.scene.render.use_simplify = False
        # culling
        bpy.context.scene.cycles.use_camera_cull = False
        bpy.context.scene.cycles.use_distance_cull = False

        self.report({'INFO'}, "Beauty preset applied for Cycles")

        return {'FINISHED'}
