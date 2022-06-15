import bpy
from bpy.types import Context, Operator

from .. import SFR_Settings
from .warning_message import draw_warning

class SFR_AnimMeshOptimization(Operator):
    bl_idname = "render.superfastrender_animbench"
    bl_label = "Animation Benchmark"
    bl_description = "Benchmarks for animations"

    def draw(self, context):
        draw_warning(self, context)

    def execute(self, context: Context):

        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings

        frame_start = scene.frame_start
        frame_end = scene.frame_end

        frame_step = settings.mo_frame_skipped

        for frame_current in range(frame_start, frame_end, frame_step):
            scene.frame_current = frame_current

            # start mesh op
            bpy.ops.render.superfastrender_meshoptim('EXEC_DEFAULT')

        self.report({'INFO'}, "Animation Mesh Optimization complete")
        return {'FINISHED'}
