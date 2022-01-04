from typing import Text
import bpy
from bpy.types import Panel
from .SFR_Settings import SFR_Settings
from .install_deps import dependencies


class SFR_PT_Panel:
    bl_label = "Super Fast Render"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {"DEFAULT_CLOSED"}

class SFR_PT_B_Panel(SFR_PT_Panel, Panel):
    bl_label = "Super Fast Render"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SHADERFX')

    def draw(self, context):
        layout = self.layout

        layout.label(text="Check Complimentary Addons", icon='INFO')
        row = layout.row()
        row.operator("initalise.complimentary")

        # Tell user they need to install dependencies
        if not dependencies.checked:
            dependencies.check_dependencies()

        if dependencies.needs_install:
            col = layout.column(align=True)
            col.label(
                text="Install dependencies",
                icon='ERROR'
            )
            col.label(
                text="       Open addon preferences and install dependencies first."
            )
            col.operator("initialise.sfr_open_addon_prefs", icon='PREFERENCES')

            return
               


class SFR_PT_RSO_Panel(SFR_PT_Panel, Panel):
    bl_label = "Render Settings Optimization"
    bl_parent_id = "SFR_PT_B_Panel"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="OPTIONS")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings
        RenderEngine = scene.render.engine
        
        if RenderEngine == "CYCLES":

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
                layout.label(text="Benchmark Settings")
                col = layout.column(align=True)
                col.prop(settings, "resolution", text="Benchmark Res", slider=True)
                col.prop(settings, "threshold", text="Threshold %", slider=True)
                col.separator()
                col.prop(settings, "frame_skipped", text="Frame Offset", slider=True)
                col.separator()

                layout.label(text="Benchmark Passes")
                col = layout.column(align=True)
                col.prop(settings, "use_diffuse", text="Diffuse",toggle=True)
                col.prop(settings, "use_glossy", text="Glossy",toggle=True)
                col.prop(settings, "use_transparent", text="Transparency",toggle=True)
                col.prop(settings, "use_transmission", text="Transmission",toggle=True)
                col.prop(settings, "use_volume", text="Volume",toggle=True)

                layout.label(text="Benchmark Light Behaviour")
                col = layout.column(align=True)
                col.prop(settings, "use_indirect", text="Indirect Brightness",toggle=True)
                col.prop(settings, "use_caustics", text="Caustic Blur",toggle=True)

                layout.label(text="Start Benchmark")
                row = layout.row()
                row.operator("render.superfastrender_benchmark", icon="RENDER_STILL")
                row.operator("render.superfastrender_animbench", icon="RENDER_ANIMATION")

                fileio = layout.column(align=True)

                fileio.prop(settings, "inputdir", text="Benchmarking Files")

        else:
            layout.label(text="This Render Engine is not supported", icon='ERROR')

class SFR_PT_TO_Panel(SFR_PT_Panel, Panel):
    bl_label = "Texture Optimizer"
    bl_parent_id = "SFR_PT_B_Panel"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="TEXTURE")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings

        layout.label(text="Texture Optimization Factor")
        col = layout.column(align=True)
        col.prop(settings, "diffuse_resize", slider=True)
        col.prop(settings, "specular_resize", slider=True)
        col.prop(settings, "roughness_resize", slider=True)
        col.prop(settings, "normal_resize", slider=True)
        col.prop(settings, "opacity_resize", slider=True)
        col.prop(settings, "translucency_resize", slider=True)
        col.separator()
        
        layout.label(text="Optimize Textures")
        row = layout.row()
        row.operator("render.superfastrender_textureoptim", icon="TEXTURE")
        row.prop(settings, "create_backup", toggle=True, icon="COPYDOWN")
        layout.label(text='To prevent damage on existing image files, your files will be copied.', icon='INFO')
        layout.label(text='you can find the copied files in the "textures" folder in the location of your .blend file', icon='INFO')
        if settings.create_backup:
            layout.label(text='the backup files will be saved in "textures backup"', icon='INFO')
        else:
            layout.label(text='the optimization step is irreversible, are you sure you do not want a backup', icon='ERROR')
     
class SFR_PT_SOCIALS_Panel(SFR_PT_Panel, Panel):
    bl_label = "Our Socials"
    bl_parent_id = "SFR_PT_B_Panel"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="FUND")

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        op = col.operator("wm.url_open", text="Join our Discord!", icon="URL")
        op.url = "https://discord.gg/cnFdGQP"
        layout.separator()        
        op = col.operator("wm.url_open", text="Our YouTube Channel!", icon="URL")
        op.url = "https://www.youtube.com/channel/UCgLo3l_ZzNZ2BCQMYXLiIOg"
        op = col.operator("wm.url_open", text="Our BlenderMarket!", icon="URL")
        op.url = "https://blendermarket.com/creators/kevin-lorengel"   
        op = col.operator("wm.url_open", text="Our Instagram Page!", icon="URL")
        op.url = "https://www.instagram.com/pidgeontools/"    
        op = col.operator("wm.url_open", text="Our Twitter Page!", icon="URL")
        op.url = "https://twitter.com/PidgeonTools"
        layout.separator()        
        op = col.operator("wm.url_open", text="Feedback", icon="URL")
        op.url = "https://discord.gg/cnFdGQP"
    
preview_collections = {}