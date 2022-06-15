import bpy
from mathutils import Vector
from bpy.types import Context, Operator
from .. import SFR_Settings
from .warning_message import draw_warning

class SFR_MeshOptimization(Operator):
    bl_idname = "render.superfastrender_meshoptim"
    bl_label = "Mesh Optimizer"
    bl_description = "Optimizes your meshes"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)
        
    def draw(self, context):
        draw_warning(self, context)
    
    def execute(self, context: Context):

        #calculate the distance between the object and the active camera
        def calculate_object_distance(selected_object_loc: Vector, active_camera_loc):
            return(selected_object_loc - active_camera_loc).length

        #a function to clamp a value between two values     
        def clamp(value, lower, upper):
            return lower if value < lower else upper if value > upper else value

        #set some variables
        settings: SFR_Settings = context.scene.sfr_settings
        active_camera_loc = bpy.context.scene.camera.location
        depsgraph = bpy.context.evaluated_depsgraph_get()

        for selected_object in bpy.context.selected_objects:
            if selected_object.type in {'MESH','CURVE', 'SURFACE', 'FONT'}:
                
                #calculate the decimation factor based on distance and polygon density
                selected_object_evaluated = selected_object.evaluated_get(depsgraph)
                selected_object_mesh = selected_object_evaluated.to_mesh()
                polygon_density = len(selected_object_mesh.polygons) / (selected_object.dimensions[0] * selected_object.dimensions[1] * selected_object.dimensions[2]) / 1000
                decimate_ratio = clamp((1-((calculate_object_distance(selected_object.location, active_camera_loc) * polygon_density) * settings.mo_quality_change / 100))**5,settings.mo_min_quality,settings.mo_max_quality)

                #Render
                if "[SFR] - Decimate" not in selected_object.modifiers and settings.mo_render_decimation:
                    #if it does not have the modfier, add it
                    decimate_modifier = selected_object.modifiers.new(name="[SFR] - Decimate", type='DECIMATE')
                    decimate_modifier.show_viewport = False
                    decimate_modifier.use_collapse_triangulate = True
                    decimate_modifier.ratio = decimate_ratio
                else:
                    #if it does have the modfier, change the ratio
                    selected_object.modifiers.get("[SFR] - Decimate").ratio = decimate_ratio
                selected_object.keyframe_insert(data_path= 'modifiers["[SFR] - Decimate"].ratio')

                #Viewport
                if "[SFR] - Decimate - Viewport" not in selected_object.modifiers and settings.mo_viewport_decimation:
                    #add a decimation modifier with a set ratio, might change it later to polygon density based ratio    
                    decimate_modifier = selected_object.modifiers.new(name="[SFR] - Decimate - Viewport", type='DECIMATE')
                    decimate_modifier.show_render = False
                    decimate_modifier.use_collapse_triangulate = True
                    decimate_modifier.ratio = settings.mo_viewport_decimation_ratio
        return {'FINISHED'}

        