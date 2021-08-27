import bpy
import sys
import subprocess
from bpy.types import Operator


class Dependencies_check_singleton(object):
    def __init__(self):
        self._checked = False
        self._error = False
        self._success = False

        self._needs_cv2 = False
        self._needs_numpy = False
        self._needs_skimage = False

    # Properties

    @property
    def checked(self):
        return self._checked

    @property
    def error(self):
        return self._error

    @property
    def success(self):
        return self._success

    @property
    def needs_install(self):
        return True in [
            self.needs_cv2,
            self.needs_numpy,
            self.needs_skimage,
        ]

    @property
    def needs_cv2(self):
        return self._needs_cv2

    @property
    def needs_numpy(self):
        return self._needs_numpy

    @property
    def needs_skimage(self):
        return self._needs_skimage

    # Methods

    def check_dependencies(self):
        self._checked = False
        self._error = False
        self._success = False

        self._needs_cv2 = False
        self._needs_numpy = False
        self._needs_skimage = False

        try:
            print("Checking for cv2...")
            import cv2
            print("cv2 found.")
        except ImportError:
            print("cv2 NOT found.")
            self._needs_cv2 = True

        try:
            print("Checking for numpy...")
            import numpy
            print("numpy found.")
        except ImportError:
            print("numpy NOT found.")
            self._needs_numpy = True

        try:
            print("Checking for scikit-image...")
            from skimage import io
            print("scikit-image found.")
        except ImportError:
            print("scikit-image NOT found.")
            self._needs_skimage = True

        self._checked = True

    def install_dependencies(self):
        self._error = False
        self._success = False

        # Update pip
        path_to_python = sys.executable if bpy.app.version > (
            2, 90) else bpy.app.binary_path_python
        try:
            print("Updating pip...")
            subprocess.run([path_to_python, "-m", "ensurepip"], check=True)
            subprocess.run([path_to_python, "-m", "pip",
                            "install", "--upgrade", "pip"], check=True)
            print("Successfully updated pip.")
        except subprocess.CalledProcessError as e:
            self._error = True
            print("Error updating pip!", e.__str__())
            # raise
            return

        # Install cv2
        if self.needs_cv2:
            try:
                print("Installing cv2...")
                subprocess.run([path_to_python, "-m", "pip", "install",
                                "--upgrade", "opencv-python"], check=True)
                subprocess.run([path_to_python, "-m", "pip", "install",
                                "--upgrade", "opencv-contrib-python"], check=True)
                import cv2
                self._needs_cv2 = False
            except (subprocess.CalledProcessError, ImportError) as e:
                self._error = True
                print("Error installing cv2!", e.__str__())
                return

        # Install numpy
        if self.needs_numpy:
            try:
                print("Installing numpy...")
                subprocess.run([path_to_python, "-m", "pip",
                                "install", "--upgrade", "numpy"], check=True)
                import numpy
                self._needs_numpy = False
            except (subprocess.CalledProcessError, ImportError) as e:
                self._error = True
                print("Error installing numpy!", e.__str__())
                return

        # Install scikit-image
        if self.needs_skimage:
            try:
                print("Installing scikit-image...")
                subprocess.run([path_to_python, "-m", "pip", "install",
                                "--upgrade", "scikit-image"], check=True)
                from skimage import io
                self._needs_skimage = False
            except (subprocess.CalledProcessError, ImportError) as e:
                self._error = True
                print("Error installing scikit-image!", e.__str__())
                return

        self._success = True


dependencies = Dependencies_check_singleton()


class SFR_OT_CheckDependencies(Operator):
    bl_idname = "initialise.sfr_check_dependencies"
    bl_label = "Check Dependencies"
    bl_description = "Checks for the Python dependencies required by the addon"

    @classmethod
    def poll(cls, context):
        return not dependencies.checked or dependencies.needs_install

    def execute(self, context):
        dependencies.check_dependencies()

        return {'FINISHED'}


class SFR_OT_InstallDependencies(Operator):
    bl_idname = "initialise.sfr_install_dependencies"
    bl_label = "Install Dependencies"
    bl_description = "Install the Python dependencies required by the addon"

    @classmethod
    def poll(cls, context):
        if not dependencies.checked:
            dependencies.check_dependencies()

        return dependencies.needs_install

    def execute(self, context):
        dependencies.install_dependencies()

        if dependencies.error:
            return {'CANCELLED'}

        return {'FINISHED'}

class SFR_OT_OpenAddonPrefs(Operator):
    bl_idname = "initialise.sfr_open_addon_prefs"
    bl_label = "Open Addon Prefs"
    bl_description = "Open the addon preferences"

    def execute(self, context):
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.context.window_manager.addon_search = "Super Fast Render"
        bpy.ops.screen.userpref_show()

        return {'FINISHED'}
