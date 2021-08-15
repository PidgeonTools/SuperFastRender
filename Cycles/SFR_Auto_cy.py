import bpy
from bpy.types import (
    Operator
)


class SFR_Auto_cy(Operator):
    bl_idname = "render.superfastrender_a"
    bl_label = "AUTOMATIC"
    bl_description = "Set the scenes automatic Optimization"

    def execute(self, context):
        self.report({'ERROR'}, "NOT YET IMPLEMENTED")
        return {'FINISHED'}
