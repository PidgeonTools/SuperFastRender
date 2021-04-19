import bpy
from bpy.types import (
    Panel,
)
from .SFR_Settings import SFR_Settings

class SFR_PT_Panel(Panel):
    bl_label = "Super Fast Render"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_category = 'Pidgeon-Tools'

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SHADERFX')
        
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings
        RenderEngine = scene.render.engine
        view_layer = context.view_layer
        cycles_view_layer = view_layer.cycles

        layout.label(text="Check Complimentary Addons", icon='ERROR')
        row = layout.row()
        row.operator("initalise.complimentary")

        detection_method = layout.column(align=True)

        detection_method.prop(
            settings,
            "detection_method",
            text="Optimization Method"
            )
        if settings.detection_method == 'MANUAL':
            detection_method.label(
                text="Sets a general optimization settings.",
                icon='INFO'
                )
            detection_method.label(
                text="       General optimization, usually requires manual tweaking."
                )
        elif settings.detection_method == 'AUTOMATIC':
            detection_method.label(
                text="Benchmarks your scene and detects which settings you roughly need.",
                icon='INFO'
                )
            detection_method.label(
                text="       EXPERIMENTAL."
                )
        layout.separator()
        
        
        
        layout = self.layout

        if settings.detection_method == 'MANUAL':
            
            layout.label(text="SUPER preset:")
            row = layout.row()
            row.operator("render.superfastrender_s")

            layout.label(text="High preset:")
            row = layout.row()
            row.operator("render.superfastrender_h")

            layout.label(text="Beauty preset:")
            row = layout.row()
            row.operator("render.superfastrender_b")
        
        else:
            col = layout.column(align=True)
            col.prop(settings, "resolution", text="Benchmark Res", slider=True)
            col.prop(settings, "threshold", text="Threshold %", slider=True)

            layout.label(text="Start Benchmark")
            row = layout.row()
            row.operator("render.superfastrender_benchmark")

            fileio = layout.column(align=True)

            fileio.prop(settings, "inputdir", text="Benchmarking Files")
            fileio.separator()
