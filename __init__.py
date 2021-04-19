bl_info = {
    "name": "Super Fast Render (SFR)",
    "author": "Kevin Lorengel",
    "version": (0, 0, 2),
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

# Register classes
classes = (
SFR_Beauty_cy,
SFR_High_cy,
SFR_Super_cy,
SFR_Auto_cy,
SFR_Benchmark_cy,
SFR_Complimentary,
SFR_PT_Panel,
SFR_Settings
)

def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.sfr_settings = PointerProperty(type=SFR_Settings, options=set())

def unregister():
    from bpy.utils import unregister_class

    del bpy.types.Scene.sfr_settings

    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
