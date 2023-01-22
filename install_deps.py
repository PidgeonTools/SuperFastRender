import bpy
import importlib
import os
import subprocess
import sys
from bpy.types import Operator
from collections import namedtuple


# functions inspired by https://github.com/robertguetzkow/blender-python-examples
Dependency = namedtuple("Dependency", ["module", "package", "name", "skip_import"])

required_dependencies = (
    Dependency(module="cv2", package="opencv-python", name="cv2", skip_import=False),
    Dependency(module="cv2", package="opencv-contrib-python", name="cv2", skip_import=False),
    Dependency(module="numpy", package="numpy", name="numpy", skip_import=False),
    Dependency(module="imagecodecs", package="imagecodecs", name="imagecodecs", skip_import=False),
    Dependency(module="skimage", package="scikit-image", name="skimage", skip_import=False),
)


def import_module(module_name, global_name=None):
    """
    Import a module.
    :param module_name: Module to import.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: ImportError and ModuleNotFoundError
    """

    if global_name is None:
        global_name = module_name

    if global_name in globals():
        importlib.reload(globals()[global_name])
    else:
        # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
        # the given name, just like the regular import would.
        globals()[global_name] = importlib.import_module(module_name)


def install_pip():
    """
    Installs pip if not already present. Please note that ensurepip.bootstrap() also calls pip, which adds the
    environment variable PIP_REQ_TRACKER. After ensurepip.bootstrap() finishes execution, the directory doesn't exist
    anymore. However, when subprocess is used to call pip, in order to install a package, the environment variables
    still contain PIP_REQ_TRACKER with the now nonexistent path. This is a problem since pip checks if PIP_REQ_TRACKER
    is set and if it is, attempts to use it as temp directory. This would result in an error because the
    directory can't be found. Therefore, PIP_REQ_TRACKER needs to be removed from environment variables.
    :return:
    """

    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)


def install_module(module_name, package_name=None):
    """
    Installs the package through pip.
    :param module_name: Module to install.
    :param package_name: (Optional) Name of the package that needs to be installed. If None it is assumed to be equal
       to the module_name.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: subprocess.CalledProcessError and ImportError
    """

    if package_name is None:
        package_name = module_name
    
    # Create a folder to install python modules
    module_path = os.path.join(os.path.dirname(__file__), "python_modules")
    if not os.path.exists(module_path):
        os.mkdir(module_path)

    # Blender disables the loading of user site-packages by default. However, pip will still check them to determine
    # if a dependency is already installed. This can cause problems if the packages is installed in the user
    # site-packages and pip deems the requirement satisfied, but Blender cannot import the package from the user
    # site-packages. Hence, the environment variable PYTHONNOUSERSITE is set to disallow pip from checking the user
    # site-packages. If the package is not already installed for Blender's Python interpreter, it will then try to.
    # The paths used by pip can be checked with `subprocess.run([sys.executable, "-m", "site"], check=True)`

    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", "--target=", module_path, package_name], check=True, env=environ_copy)
    

class Dependencies_check_singleton(object):
    def __init__(self):
        self._checked = False
        self._needs_install = False
        self._error = False
        self._success = False

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
        return self._needs_install

    # Methods

    def check_dependencies(self):
        self._checked = False

        try:
            for dependency in required_dependencies:
                if dependency.skip_import: continue
                print(f"Checking for {dependency.module}...")
                import_module(dependency.module, dependency.name)
                print(f"Found {dependency.module}.")
            self._needs_install = False
        except ModuleNotFoundError:
            print("One or more dependencies need to be installed.")
            self._needs_install = True

        self._checked = True

    def install_dependencies(self):
        self._error = False
        self._success = False

        # Update pip
        print("Ensuring pip is installed...")
        install_pip()

        for dependency in required_dependencies:
            package_name = dependency.package if dependency.package is not None else dependency.module
            print(f"Installing {package_name}...")
            try:
                install_module(module_name=dependency.module, package_name=dependency.package)
            except (subprocess.CalledProcessError, ImportError) as err:
                self._error = True
                print(f"Error installing {package_name}!")
                print(str(err))
                raise ValueError(package_name)

        self._success = True

        self.check_dependencies()


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
        try:
            dependencies.install_dependencies()
        except ValueError as ve:
            self.report({"ERROR"}, f"Error installing package {ve.args[0]}.\n\nCheck the System Console for details.")

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
