import bpy
from bpy.types import Context, Operator
import os
nc = os.path.normcase
from distutils.dir_util import copy_tree
from .. import SFR_Settings
from .SFR_ImageResizer import resize_image

class SFR_TextureOptimizer(Operator):
    bl_idname = "render.superfastrender_textureoptim"
    bl_label = "Texture Optimizer"
    bl_description = "Optimizes your textures"

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
        AO = ["ao","ambient occlusion","occlusion"]

        #make skimage not give warning
        import imageio.core.util
        def ignore_warnings(*args, **kwargs):
            pass
        imageio.core.util._precision_warn = ignore_warnings

        print("TEXTURE OPTIMIZATION: INITIALIZED")

        # Don't resize the same file more than once, in case the name matches more than one type
        seen = {} # file => [Diffuse, Specular, ...]
        def add_to_seen(file, type):
            if not file in seen:
                seen[file] = []
            seen[file].append(type)
            if len(seen[file]) > 1:
                types = ", ".join(seen[file])
                print(f'Warning: image file "{file}" matches multiple texture types: {types}! Will not resize again.')
                return True

            return False

        def do_resize(path, setting, prop, type):
            for file in os.listdir(path):
                if not os.path.isfile(os.path.join(path, file)):
                    continue
                # lowercase file name for comparisons
                nc_file = nc(file)

                if setting > 0:
                    if [name for name in prop if name in nc_file]:
                        if add_to_seen(file, type):
                            continue
                        resize_image(file, setting, path)
            
        do_resize(path, settings.diffuse_resize, Diffuse, 'Diffuse')
        do_resize(path, settings.ao_resize, AO, 'AO')
        do_resize(path, settings.specular_resize, Specular, 'Specular')
        do_resize(path, settings.roughness_resize, Roughness, 'Roughness')
        do_resize(path, settings.opacity_resize, Opacity, 'Opacity')
        do_resize(path, settings.normal_resize, Normal, 'Normal')
        do_resize(path, settings.translucency_resize, Translucency, 'Translucency')
                
        print("TEXTURE OPTIMIZATION: COMPLETED")

        return {'FINISHED'}
