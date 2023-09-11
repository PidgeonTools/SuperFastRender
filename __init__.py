# To make sure installed modules work
import os, sys
module_path = os.path.join(os.path.dirname(__file__), "python_modules")
sys.path.append(module_path) # Add a module path for this specific addon

import bpy
from bpy.props import (
    PointerProperty,
    BoolProperty,
    IntProperty
)
from .install_deps import (
    dependencies,
    SFR_OT_CheckDependencies,
    SFR_OT_InstallDependencies,
    SFR_OT_OpenAddonPrefs,
)
from .SFR_Settings import SFR_Settings
from .SRF_Complimentary import SFR_Complimentary
from .Cycles.SFR_Benchmark_cy import SFR_Benchmark_cy
from .Utils.SFR_AnimationBenchmark import SFR_AnimationBenchmark
from .Cycles.SFR_Super_cy import SFR_Super_cy
from .Cycles.SFR_High_cy import SFR_High_cy
from .Cycles.SFR_Beauty_cy import SFR_Beauty_cy
from .SFR_Panel import SFR_PT_B_Panel, SFR_PT_RSO_Panel, SFR_PT_TO_Panel, SFR_PT_SOCIALS_Panel
from .Utils.SFR_TextureOptimizer import SFR_TextureOptimizer

from . import addon_updater_ops

bl_info = {
    "name": "Super Fast Render (SFR)",
    "author": "Kevin Lorengel, Chris Bond (Kamikaze)",
    "version": (3, 1, 3),
    "blender": (2, 92, 0),
    "location": "Properties > Render > Super Fast Render",
    "description": "SFR optimizes your scene, so you render faster!",
    "warning": "IN DEV VERSION",
    "wiki_url": "https://discord.gg/cnFdGQP",
    "endpoint_url": "https://raw.githubusercontent.com/PidgeonTools/SAM-Endpoints/main/SuperFastRender.json",
    "tracker_url": "https://github.com/PidgeonTools/SuperFastRender/issues",
    "category": "Render",
}


class SIDPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # addon updater preferences

    auto_check_update: BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months: IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days: IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours: IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes: IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)

        if not dependencies.checked or dependencies.needs_install:
            if dependencies.error:
                col.label(text="Installing dependencies failed.")
                col.label(text="Check Blender's System Console or your terminal for errors.")
                col.separator()

            col = layout.column(align=True)
            col.label(
                text="Installation may take a few minutes, and Blender will " \
                    "stop responding during this time.")
            col.label(text="If the Install Dependencies button is still visible after this process completes, please restart Blender.")

            col.operator("initialise.sfr_install_dependencies")
        else:
            col.label(text="Dependencies installed!")
        col.separator()

        col = layout.column()  # works best if a column, or even just self.layout

        # updater draw function
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context, col)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # col.operator("wm.url_open","Open webpage ").url=addon_updater_ops.updater.website


classes = (
    SFR_Beauty_cy,
    SFR_High_cy,
    SFR_Super_cy,
    SFR_Benchmark_cy,
    SFR_Complimentary,
    SFR_PT_B_Panel,
    SFR_PT_RSO_Panel,
    SFR_PT_TO_Panel,
    SFR_PT_SOCIALS_Panel,
    SFR_Settings,
    SFR_OT_CheckDependencies,
    SFR_OT_InstallDependencies,
    SIDPreferences,
    SFR_AnimationBenchmark,
    SFR_OT_OpenAddonPrefs,
    SFR_TextureOptimizer
)


def register(): 
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)

    dependencies.check_dependencies()

    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(
            cls)  # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)

    bpy.types.Scene.sfr_settings = PointerProperty(
        type=SFR_Settings, options=set())
   
def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()

    del bpy.types.Scene.sfr_settings

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
