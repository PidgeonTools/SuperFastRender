import bpy
from bpy.types import Context, Operator

class SFR_MeshOptimizationRemove(Operator):
    bl_idname = "render.superfastrender_meshoptimremove"
    bl_label = "Mesh Optimize Remover"
    bl_description = "Removes Mesh Optimization"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        layout = self.layout
        layout.label(text = "This action can take a while.")
        layout.label(text = "We recommend you open the System Console, if you are on Windows.")
        layout.label(text = 'To do so, go to your top bar "Window" -> "Toggle System Console"')
        layout.label(text = "There you will be able to see the progress.")
        layout.separator()
        layout.label(text = "Blender will appear to freeze, please be patient.")
        layout.separator()
        layout.label(text = "To proceed with the optimization, press [OK]")
        
    def execute(self, context: Context):
        for selected_object in bpy.context.selected_objects:
            if "[SFR] - Decimate" not in selected_object.modifiers:
                continue
            else:
                selected_object.modifiers.remove(selected_object.modifiers.get("[SFR] - Decimate"))
        return{'FINISHED'}


        