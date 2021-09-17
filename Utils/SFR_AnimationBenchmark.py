import bpy
from bpy.types import (
    Operator
)

from .. import SFR_Settings


class SFR_AnimationBenchmark(Operator):
    bl_idname = "render.superfastrender_animbench"
    bl_label = "Animation Benchmark"
    bl_description = "Benchmarks for animations"

    def execute(self, context):

        scene = bpy.context.scene
        settings: SFR_Settings = scene.sfr_settings
        keyframe_insert = bpy.context.window.scene.keyframe_insert
        frame_current = bpy.context.scene.frame_current
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end

        frame_skipped = settings.frame_skipped

        max_bounces = []
        diffuse_bounces = []
        glossy_bounces = []
        transmission_bounces = []
        transparent_bounces = []
        volume_bounces = []
        clamp_indirect = []
        caustic_blur = []
        vol_steps = []


        if scene.render.engine == 'CYCLES':
            
            prefs = bpy.context.preferences.addons['cycles'].preferences
            cycles = scene.cycles

            for frame_current in range(frame_start, frame_end, frame_skipped):
                
                scene.frame_current = frame_current

                # start benchmark
                bpy.ops.render.superfastrender_benchmark()

                max_bounces.append(cycles.max_bounces)
                diffuse_bounces.append(cycles.diffuse_bounces)
                glossy_bounces.append(cycles.glossy_bounces)
                transmission_bounces.append(cycles.transmission_bounces)
                transparent_bounces.append(cycles.transparent_max_bounces)
                volume_bounces.append(cycles.volume_bounces)
                clamp_indirect.append(cycles.sample_clamp_indirect)
                caustic_blur.append(cycles.blur_glossy)
                vol_steps.append(cycles.volume_max_steps)

            for frame_current in range(frame_start, frame_end, frame_skipped):
                
                # key max bounces
                cycles.max_bounces = max_bounces[0]
                del max_bounces[0]
                keyframe_insert('cycles.max_bounces', frame=frame_current)

                if settings.use_diffuse:
                    cycles.diffuse_bounces = diffuse_bounces[0]
                    del diffuse_bounces[0]
                    keyframe_insert('cycles.diffuse_bounces', frame=frame_current)

                if settings.use_glossy:
                    cycles.glossy_bounces = glossy_bounces[0]
                    del glossy_bounces[0]
                    keyframe_insert('cycles.glossy_bounces', frame=frame_current)

                if settings.use_transparent:
                    cycles.transparent_max_bounces = transparent_bounces[0]
                    del transparent_bounces[0]
                    keyframe_insert('cycles.transparent_max_bounces', frame=frame_current)

                if settings.use_transmission:
                    cycles.transmission_bounces = transmission_bounces[0]
                    del transmission_bounces[0]
                    keyframe_insert('cycles.transmission_bounces', frame=frame_current)

                if settings.use_indirect:
                    cycles.sample_clamp_indirect = clamp_indirect[0]
                    del clamp_indirect[0]
                    keyframe_insert('cycles.sample_clamp_indirect', frame=frame_current)

                if settings.use_caustics:
                    cycles.blur_glossy = caustic_blur[0]
                    del caustic_blur[0]
                    keyframe_insert('cycles.blur_glossy', frame=frame_current)

                if settings.use_volume:
                    cycles.volume_bounces = volume_bounces[0]
                    del volume_bounces[0]
                    cycles.volume_max_steps = vol_steps[0]
                    del vol_steps[0]
                    keyframe_insert('cycles.volume_bounces', frame=frame_current)
                    keyframe_insert('cycles.volume_max_steps', frame=frame_current)

            self.report({'INFO'}, "Animation benchmark complete")

            return {'FINISHED'}