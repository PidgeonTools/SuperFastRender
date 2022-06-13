import bpy
from mathutils import Vector
from bpy.types import Context, Operator
from .. import SFR_Settings

class SFR_MeshOptimization(Operator):
    bl_idname = "render.superfastrender_meshoptim"
    bl_label = "Mesh Optimizer"
    bl_description = "Optimizes your meshes"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        layout = self.layout
        layout.label(text = "Optimizing your meshes can take a while.")
        layout.label(text = "We recommend you open the System Console, if you are on Windows.")
        layout.label(text = 'To do so, go to your top bar "Window" -> "Toggle System Console"')
        layout.label(text = "There you will be able to see the progress.")
        layout.separator()
        layout.label(text = "Blender will appear to freeze, please be patient.")
        layout.separator()
        layout.label(text = "To proceed with the optimization, press [OK]")
    
    def execute(self, context: Context):

        def calculate_object_distance(selected_object_loc: Vector, active_camera_loc):
            return(selected_object_loc - active_camera_loc).length
                
        def clamp(value, lower, upper):
            return lower if value < lower else upper if value > upper else value

        settings: SFR_Settings = context.scene.sfr_settings
        active_camera_loc = bpy.context.scene.camera.location
        depsgraph = bpy.context.evaluated_depsgraph_get()

        for selected_object in bpy.context.selected_objects:
            if selected_object.type in {'MESH','CURVE', 'SURFACE', 'FONT'}:

                selected_object_evaluated = selected_object.evaluated_get(depsgraph)
                selected_object_mesh = selected_object_evaluated.to_mesh()

                polygon_density = len(selected_object_mesh.polygons) / (selected_object.dimensions[0] * selected_object.dimensions[1] * selected_object.dimensions[2]) / 1000
                print(polygon_density)
                decimate_ratio = clamp((1-((calculate_object_distance(selected_object.location, active_camera_loc) * polygon_density) * settings.mo_quality_change / 100))**5,settings.mo_min_quality,settings.mo_max_quality)
    
                if "[SFR] - Decimate" not in selected_object.modifiers:
                    decimate_modifier = selected_object.modifiers.new(name="[SFR] - Decimate", type='DECIMATE')
                    decimate_modifier.show_viewport = False
                    decimate_modifier.ratio = decimate_ratio
                else:
                    selected_object.modifiers.get("[SFR] - Decimate").ratio = decimate_ratio
                selected_object.keyframe_insert(data_path= 'modifiers["[SFR] - Decimate"].ratio')
        return {'FINISHED'}

        