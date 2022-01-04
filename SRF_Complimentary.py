import bpy
from bpy.types import (
    Operator
)

import addon_utils

import webbrowser


class SFR_Complimentary(Operator):
    bl_idname = "initalise.complimentary"
    bl_label = "Complimentary Addons"

    GetSID: bpy.props.BoolProperty(name="Enable / Download SID", default=True)
    #GetSRR: bpy.props.BoolProperty(name="Enable / Download SRR", default=True)
    ComputeDevice: bpy.props.BoolProperty(
        name="Detect Best Compute Device", default=True)

    def execute(self, context):
        # SID helps with denoising
        if self.GetSID:
            if 'Super Image Denoiser (SID)' in bpy.context.preferences.addons:
                addon_utils.enable('Super Image Denoiser (SID)', default_set=True)
            else:
                webbrowser.open(
                    'https://gumroad.com/l/superimagedenoiser', new=2)

        # SRR helps with large resolutions
        # if self.GetSID:
        #    if 'SuperResRender' in bpy.context.preferences.addons:
        #        print('Detected SRR')
        #        addon_utils.enable('SuperResRender', default_set=True)
        #    else:
        #        print('SRR not detected opening download link')
        #        webbrowser.open('https://gumroad.com/l/superresrender', new=2)

        # SFR detects best compute device
        if self.ComputeDevice:
            prefs = bpy.context.preferences.addons['cycles'].preferences

            for device_type in prefs.get_device_types(bpy.context):

                prefs.get_devices_for_type(device_type[0])

        # NVIDIA RTX
            if prefs.get_devices_for_type:
                'OPTIX'
                prefs.compute_device_type = "OPTIX"
        # NVIDIA
            elif prefs.get_devices_for_type:
                'CUDA'
                prefs.compute_device_type = "CUDA"
        # AMD
            elif prefs.get_devices_for_type:
                'OPENCL'
                prefs.compute_device_type = "OPENCL"

        return {'FINISHED'}

    def invoke(self, context, event):
        OpenWindow = context.window_manager
        return OpenWindow.invoke_props_dialog(self)
