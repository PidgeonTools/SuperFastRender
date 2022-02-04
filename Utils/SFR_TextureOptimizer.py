import bpy
from bpy.types import Context, Operator
import os
nc = os.path.normcase
import imageio.core.util
from distutils.dir_util import copy_tree
from .. import SFR_Settings
from .SFR_ImageResizer import resize_image

class SFR_TextureOptimizer(Operator):
    bl_idname = "render.superfastrender_textureoptim"
    bl_label = "Texture Optimizer"
    bl_description = "Optimizes your textures"

    #make skimage not give warning
    def ignore_warnings(*args, **kwargs):
        pass
    imageio.core.util._precision_warn = ignore_warnings

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self,context):
        layout = self.layout
        layout.label(text = "Optimizing your textures can take a while.")
        layout.label(text = "We recommend you open the System Console, if you are on Windows.")
        layout.label(text = 'To do so, go to your top bar "Window" -> "Toggle System Console"')
        layout.label(text = "There you will be able to see the progress.")
        layout.separator()
        layout.label(text = "Blender will appear to freeze, please be patient.")
        layout.separator()
        layout.label(text = "To proceed with the optimization, press [OK]")

    def execute(self, context: Context):
        
        #put all images into one folder
        bpy.ops.file.pack_all()
        bpy.ops.file.unpack_all(method="USE_LOCAL")
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings
        path = bpy.path.abspath("//textures/")

        if settings.create_backup:
            fromDirectory = path
            toDirectory = bpy.path.abspath("//textures backup/")
            copy_tree(fromDirectory, toDirectory)

        Diffuse = ["albedo","col","diffuse","diff","dif"]
        Specular = ["specular","spec","reflection","refl","metallic","metalness","metal","met"]
        Roughness = ["roughness","rough","glossiness","gloss"]
        Opacity = ["opacity","alpha","presence"]
        Normal = ["normal","norm","nor","nrm","bump","bmp","height"]
        Translucency = ["translucency","transmission","translucent"]

        print("TEXTURE OPTIMIZATION: INITIALIZED")

        if settings.diffuse_resize > 0:
            currDiffuse = 0
            for eachName in Diffuse:
                for iFiles in os.listdir(path):
                    if os.path.isfile(nc(os.path.join(path,iFiles))) and Diffuse[currDiffuse] in nc(iFiles):
                            settings.resize_image(iFiles, settings.diffuse_resize, path)
                currDiffuse += 1

        if settings.specular_resize > 0:
            currSpecular = 0
            for eachName in Specular:
                for iFiles in os.listdir(path):
                    if os.path.isfile(nc(os.path.join(path,iFiles))) and Specular[currSpecular] in nc(iFiles):
                            resize_image(iFiles, settings.specular_resize, path)
                currSpecular += 1

        if settings.roughness_resize > 0:
            currRoughness = 0
            for eachName in Roughness:
                for iFiles in os.listdir(path):
                    if os.path.isfile(nc(os.path.join(path,iFiles))) and Roughness[currRoughness] in nc(iFiles):
                        resize_image(iFiles, settings.roughness_resize, path)
                currRoughness += 1

        if settings.opacity_resize > 0:
            currOpacity = 0
            for eachName in Opacity:
                for iFiles in os.listdir(path):
                    if os.path.isfile(nc(os.path.join(path,iFiles))) and Opacity[currOpacity] in nc(iFiles):
                        resize_image(iFiles, settings.opacity_resize, path)
                currOpacity += 1

        if settings.normal_resize > 0:
            currNormal = 0
            for eachName in Normal:
                for iFiles in os.listdir(path):
                    if os.path.isfile(nc(os.path.join(path,iFiles))) and Normal[currNormal] in nc(iFiles):
                        resize_image(iFiles, settings.normal_resize, path)
                currNormal += 1

        if settings.translucency_resize > 0:
            currTranslucency = 0
            for eachName in Translucency:
                for iFiles in os.listdir(path):
                    if os.path.isfile(nc(os.path.join(path,iFiles))) and Translucency[currTranslucency] in nc(iFiles):
                        resize_image(iFiles, settings.translucency_resize, path)
                currTranslucency += 1

        print("TEXTURE OPTIMIZATION: COMPLETED")

        return {'FINISHED'}
