bl_info = {
    "name": "Super Fast Render (SFR)",
    "author": "Kevin Lorengel",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "location": "Properties > Render > Super Fast Render",
    "description": "SFR optimizes your scene, so you render faster!",
    "warning": "",
    "wiki_url": "https://discord.gg/cnFdGQP",
    "category": "Render",
}

import bpy
from .SFR_Panel import SFR_PT_Panel
from .Cycles.SFR_Beauty_cy import SFR_Beauty_cy
from .Cycles.SFR_High_cy import SFR_High_cy
from .Cycles.SFR_Super_cy import SFR_Super_cy
from .Cycles.SFR_Auto_cy import SFR_Auto_cy
from .Cycles.SFR_Benchmark_cy import SFR_Benchmark_cy
from .SRF_Complimentary import SFR_Complimentary
from .SFR_Settings import SFR_Settings
from bpy.props import (
    PointerProperty,
)
from . import addon_updater_ops

class DemoPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
        )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
        )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
        )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
        )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
        )

    def draw(self, context):
        layout = self.layout
        # col = layout.column() # works best if a column, or even just self.layout
        mainrow = layout.row()
        col = mainrow.column()

        # updater draw function
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context)

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
    SFR_Auto_cy,
    SFR_Benchmark_cy,
    SFR_Complimentary,
    SFR_PT_Panel,
    SFR_Settings,
    DemoPreferences
)

def register():
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)

    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(cls) # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)

    bpy.types.Scene.sfr_settings = PointerProperty(type=SFR_Settings, options=set())

def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()
    
    del bpy.types.Scene.sfr_settings

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

