import typing
import os
import bpy
import bpy.utils.previews
from bpy.types import Panel
from .SFR_Settings import SFR_Settings
from .install_deps import dependencies

ICON_DIR_NAME = "Icons"

class IconManager:
    def __init__(self, additional_paths: typing.Optional[typing.List[str]] = None):
        self.icon_previews = bpy.utils.previews.new()
        self.additional_paths = additional_paths if additional_paths is not None else []
        self.load_all()

    def load_all(self) -> None:
        icons_dir = os.path.join(os.path.dirname(__file__), ICON_DIR_NAME)
        self.load_icons_from_directory(icons_dir)

        for path in self.additional_paths:
            self.load_icons_from_directory(os.path.join(path, ICON_DIR_NAME))

    def load_icons_from_directory(self, path: str) -> None:
        if not os.path.isdir(path):
            raise RuntimeError(f"Cannot load icons from {path}, it is not valid dir")

        for icon_filename in os.listdir(path):
            self.load_icon(icon_filename, path)

    def load_icon(self, filename: str, path: str) -> None:
        if not filename.endswith((".png")):
            return

        icon_basename, _ = os.path.splitext(filename)
        if icon_basename in self.icon_previews:
            return

        self.icon_previews.load(icon_basename, os.path.join(
            path, filename), "IMAGE")

    def get_icon(self, icon_name: str) -> bpy.types.ImagePreview:
        return self.icon_previews[icon_name]

    def get_icon_id(self, icon_name: str) -> int:
        return self.icon_previews[icon_name].icon_id


icon_manager = IconManager()



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
            layout.active = not dependencies.needs_install

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

        layout.active = not dependencies.needs_install

        layout.label(text="Texture Optimization Factor")
        col = layout.column(align=True)
        col.prop(settings, "diffuse_resize", slider=True)
        col.prop(settings, "ao_resize", slider=True)
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
        layout.label(text='To prevent overwriting existing image files, your files will be copied.', icon='INFO')
        layout.label(text='You can find the copied files in the "textures" folder in the location of your .blend file.', icon='INFO')
        if settings.create_backup:
            layout.label(text='The backup files will be saved in "textures backup".', icon='INFO')
        else:
            layout.label(text='The optimization step is irreversible, are you sure you do not want a backup?', icon='ERROR')

class SFR_PT_MO_Panel(SFR_PT_Panel, Panel):
    bl_label = "Mesh Optimizer"
    bl_parent_id = "SFR_PT_B_Panel"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="MESH_ICOSPHERE")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings

        layout.active = not dependencies.needs_install

        layout.label(text="Mesh Optimization Settings")
        col = layout.column(align=True)
        col.prop(settings, "mo_render_decimation")
        col.prop(settings, "mo_viewport_decimation")
        col.separator()

        col.prop(settings, "mo_max_quality", slider=True)
        col.prop(settings, "mo_min_quality", slider=True)
        col.prop(settings, "mo_quality_change", slider=True)
        col.separator()
        col.prop(settings, "mo_viewport_decimation_ratio", slider=True)
        col.separator()
        col.prop(settings, "mo_frame_skipped", slider=True)
        col.separator()

        layout.label(text="Optimize Meshes")
        row = layout.row()
        row.operator("render.superfastrender_meshoptim", icon="MESH_ICOSPHERE", text="Frame Optimization")
        row.operator("render.superfastrender_animbench", icon="MESH_UVSPHERE", text="Animation Optimization")
        row.operator("render.superfastrender_meshoptimremove", icon="LOOP_BACK", text="Remove Optimization")

class SFR_PT_SOCIALS_Panel(SFR_PT_Panel, Panel):
    bl_label = "Our Socials"
    bl_parent_id = "SFR_PT_B_Panel"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon="FUND")

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator(
            "wm.url_open",
            text="Join our Discord!",
            icon_value = icon_manager.get_icon_id("Discord")
            ).url = "https://discord.gg/cnFdGQP"
        layout.separator()

        col.operator(
            "wm.url_open",
            text="Our YouTube Channel!",
            icon_value = icon_manager.get_icon_id("Youtube")
            ).url = "https://www.youtube.com/channel/UCgLo3l_ZzNZ2BCQMYXLiIOg"
        col.operator(
            "wm.url_open",
            text="Our BlenderMarket!",
            icon_value = icon_manager.get_icon_id("BlenderMarket")
            ).url = "https://blendermarket.com/creators/kevin-lorengel"   
        col.operator(
            "wm.url_open",
            text="Our Instagram Page!",
            icon_value = icon_manager.get_icon_id("Instagram")
            ).url = "https://www.instagram.com/pidgeontools/"    
        col.operator(
            "wm.url_open",
            text="Our Twitter Page!",
            icon_value = icon_manager.get_icon_id("Twitter")
            ).url = "https://twitter.com/PidgeonTools"
        layout.separator()

        col.operator(
            "wm.url_open",
            text="Support and Feedback!",
            icon="HELP"
            ).url = "https://discord.gg/cnFdGQP"

preview_collections = {}
