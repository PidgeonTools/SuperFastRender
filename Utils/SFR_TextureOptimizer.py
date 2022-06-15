from sys import base_prefix
import bpy
from bpy.types import Context, Image, Operator
import os
nc = os.path.normcase
from distutils.dir_util import copy_tree
import pathlib
from .. import SFR_Settings
from ..install_deps import dependencies
from .SFR_ImageResizer import resize_image
from .warning_message import draw_warning

class SFR_TextureOptimizer(Operator):
    bl_idname = "render.superfastrender_textureoptim"
    bl_label = "Texture Optimizer"
    bl_description = "Optimizes your textures"

    @classmethod
    def poll(cls, context: Context):
        if not dependencies.checked or dependencies.needs_install:
            dependencies.check_dependencies()

        return not dependencies.needs_install

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        draw_warning(self, context)

    def execute(self, context: Context):
        # put all images into one folder
        bpy.ops.file.pack_all()
        bpy.ops.file.unpack_all(method="USE_LOCAL")
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings
        base_path_relative = "//textures/"
        path = bpy.path.abspath(base_path_relative)

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

        # make skimage not give warning
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

        def resize_if_not_seen(path, file, nc_file, setting, prop, type):
            if setting > 0:
                if [name for name in prop if name in nc_file]:
                    if add_to_seen(file, type):
                        return True
                    resize_image(file, setting, path)
                    return True
            return False

        def remap_image_texture(base_path_relative, file, nc_file):
            # image format was converted to PNG; we now need to point at the new PNG file
            orig_path = base_path_relative + file
            orig_nc_path = base_path_relative + nc_file
            png_file = str(pathlib.Path(file).with_suffix(".png"))
            for img in bpy.data.images: # type: Image
                if img.filepath in (orig_path, orig_nc_path):
                    img.filepath = base_path_relative + png_file
                    img.reload()


        for file in os.listdir(path):
            if not os.path.isfile(os.path.join(path, file)):
                continue
            # lowercase file name for comparisons
            nc_file = nc(file)

            results = [
                resize_if_not_seen(path, file, nc_file, settings.diffuse_resize, Diffuse, 'Diffuse'),
                resize_if_not_seen(path, file, nc_file, settings.ao_resize, AO, 'AO'),
                resize_if_not_seen(path, file, nc_file, settings.specular_resize, Specular, 'Specular'),
                resize_if_not_seen(path, file, nc_file, settings.roughness_resize, Roughness, 'Roughness'),
                resize_if_not_seen(path, file, nc_file, settings.opacity_resize, Opacity, 'Opacity'),
                resize_if_not_seen(path, file, nc_file, settings.normal_resize, Normal, 'Normal'),
                resize_if_not_seen(path, file, nc_file, settings.translucency_resize, Translucency, 'Translucency'),
            ]
            if True in results:
                remap_image_texture(base_path_relative, file, nc_file)

        print("TEXTURE OPTIMIZATION: COMPLETED")

        return {'FINISHED'}
