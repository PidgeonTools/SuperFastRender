import bpy
from bpy.types import Context, Operator

from .. import SFR_Settings


class SFR_AnimationBenchmark(Operator):
    bl_idname = "render.superfastrender_animbench"
    bl_label = "Animation Benchmark"
    bl_description = "Benchmarks for animations"

    @classmethod
    def poll(cls, context: Context):
        return context.scene.render.engine == 'CYCLES'

    def execute(self, context: Context):

        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings

        frame_start = scene.frame_start
        frame_end = scene.frame_end

        frame_step = settings.frame_skipped

        if scene.render.engine == 'CYCLES':
            for frame_current in range(frame_start, frame_end, frame_step):
                scene.frame_current = frame_current

                # start benchmark
                bpy.ops.render.superfastrender_benchmark('EXEC_DEFAULT', insert_keyframes=True)

        else:
            self.report({'WARNING'}, "Current render engine is not supported")
            return {'CANCELLED'}

        self.report({'INFO'}, "Animation benchmark complete")
        return {'FINISHED'}
