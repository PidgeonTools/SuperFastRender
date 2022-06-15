import bpy
from bpy.types import Context, Operator
from .warning_message import draw_warning

class SFR_MeshOptimizationRemove(Operator):
    bl_idname = "render.superfastrender_meshoptimremove"
    bl_label = "Mesh Optimize Remover"
    bl_description = "Removes Mesh Optimization"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)


    def draw(self, context):
        draw_warning(self, context)
        
    def execute(self, context: Context):
        for selected_object in bpy.context.selected_objects:
            if "[SFR] - Decimate" not in selected_object.modifiers:
                continue
            else:
                selected_object.modifiers.remove(selected_object.modifiers.get("[SFR] - Decimate"))
                
            if "[SFR] - Decimate - Viewport" not in selected_object.modifiers:
                continue
            else:
                selected_object.modifiers.remove(selected_object.modifiers.get("[SFR] - Decimate - Viewport"))
        return{'FINISHED'}


        