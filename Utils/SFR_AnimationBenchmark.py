import bpy
from bpy.types import (
    Operator
)

from .. import SFR_Settings
from .. import SFR_Benchmark_cy

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

        if scene.render.engine == 'CYCLES':
            
            prefs = bpy.context.preferences.addons['cycles'].preferences
            cycles = scene.cycles

            for frame_current in range(frame_start, frame_end, frame_skipped):
                
                # save settings for optimization

                # remember max bounces
                prev_max_bounces = cycles.max_bounces
                prev_diffuse_bounces = cycles.diffuse_bounces
                prev_glossy_bounces = cycles.glossy_bounces
                prev_transparent_bounces = cycles.transparent_max_bounces
                prev_transmission_bounces = cycles.transmission_bounces
                prev_volume_bounces = cycles.volume_bounces

                # remember clamps to reduce fireflies
                prev_clamp_direct = cycles.sample_clamp_direct
                prev_clamp_indirect = cycles.sample_clamp_indirect

                # remember caustic settings
                prev_caustic_blur = cycles.blur_glossy

                # change volume settings
                prev_col_max = cycles.volume_max_steps
                
                # start benchmark
                SFR_Benchmark_cy.execute(self,context)
                
                # key max bounces
                #if not prev_max_bounces == cycles.max_bounces:
                keyframe_insert('cycles.max_bounces', frame=frame_current)
                #if not prev_diffuse_bounces == cycles.diffuse_bounces: 
                keyframe_insert('cycles.diffuse_bounces', frame=frame_current)
                #if not prev_glossy_bounces == cycles.glossy_bounces:
                keyframe_insert('cycles.glossy_bounces', frame=frame_current)
                #if not prev_transparent_bounces == cycles.transparent_max_bounces:
                keyframe_insert('cycles.transparent_max_bounces', frame=frame_current)
                #if not prev_transmission_bounces == cycles.transmission_bounces:
                keyframe_insert('cycles.transmission_bounces', frame=frame_current)
                #if not prev_volume_bounces == cycles.volume_bounces:
                keyframe_insert('cycles.volume_bounces', frame=frame_current)
                

                # key clamps to reduce fireflies
                #if not prev_clamp_indirect == cycles.sample_clamp_indirect:
                keyframe_insert('cycles.sample_clamp_indirect', frame=frame_current)

                # key caustic settings
                #if not prev_caustic_blur == cycles.blur_glossy:
                keyframe_insert('cycles.blur_glossy', frame=frame_current)

                # key volume settings
                #if not prev_col_max == cycles.volume_max_steps:
                keyframe_insert('cycles.volume_max_steps', frame=frame_current)

                print("######################################################### Finished Frame: ", frame_current)
            self.report({'INFO'}, "Animation benchmark complete")

            return {'FINISHED'}
