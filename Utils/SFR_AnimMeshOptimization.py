import bpy
from bpy.types import Context, Operator

from .. import SFR_Settings

class SFR_AnimMeshOptimization(Operator):
    bl_idname = "render.superfastrender_animbench"
    bl_label = "Animation Benchmark"
    bl_description = "Benchmarks for animations"

    def draw(self,context):
        layout = self.layout
        layout.label(text = "Benchmarking your scene can take a while.")
        layout.label(text = "We recommend you open the System Console, if you are on Windows.")
        layout.label(text = 'To do so, go to your top bar "Window" -> "Toggle System Console"')
        layout.label(text = "There you will be able to see the progress.")
        layout.separator()
        layout.label(text = "Blender will appear to freeze, please be patient.")
        layout.separator()
        layout.label(text = "To proceed with the benchmark, press [OK]")

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
