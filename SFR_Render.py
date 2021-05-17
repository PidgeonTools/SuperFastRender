import subprocess
import os
<<<<<<< Updated upstream
from typing import Dict, List, NamedTuple, Type
import bpy
from enum import Enum
=======
import bpy
>>>>>>> Stashed changes

from . import SFR_Settings

from bpy.types import (
    Operator,
<<<<<<< Updated upstream
    Scene,
=======
>>>>>>> Stashed changes
    Timer
)

subprocess.run([bpy.app.binary_path_python, "-m", "ensurepip"], check=True)
subprocess.run([bpy.app.binary_path_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)

try:
    import cv2
    print("success cv2")
except ImportError:
    print("downloading cv2")
    subprocess.run([bpy.app.binary_path_python, "-m", "pip", "install", "--upgrade", "opencv-python"], check=True)
    subprocess.run([bpy.app.binary_path_python, "-m", "pip", "install", "--upgrade", "opencv-contrib-python"], check=True)
    import cv2
    print("success cv2")
    
try:
    import numpy as np
    print("success numpy")
except ImportError:
    print("downloading numpy")
    subprocess.run([bpy.app.binary_path_python, "-m", "pip", "install", "--upgrade", "numpy"], check=True)
    import numpy as np
    print("success numpy")

try:
    from skimage import io
    print("success skimage")
except ImportError:
    print("downloading skimage")
    subprocess.run([bpy.app.binary_path_python, "-m", "pip", "install", "--upgrade", "scikit-image"], check=True)
    from skimage import io
    print("success numpy")



<<<<<<< Updated upstream
class Shot(str, Enum):
    DIFFUSE = 'DIFFUSE'
    GLOSSY = 'GLOSSY'
    TRANSMISSION = 'TRANSMISSION'
    TRANSPARENCY = 'TRANSPARENCY'
    VOLUME = 'VOLUME'
    CLAMP_INDIRECT = 'CLAMP_INDIRECT'
    CAUSTIC_BLUR = 'CAUSTIC_BLUR'
    CAUSTIC_REFLECTIVE = 'CAUSTIC_REFLECTIVE'
    CAUSTIC_REFRACTIVE = 'CAUSTIC_REFRACTIVE'

class TestShot:
    scene: Scene

    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def next(self) -> bool:
        ''' `True` if the operation succeeded, or `False` if it could not determine a next value '''
        return True

    def back(self) -> None:
        pass

def make_cycles_simple_numeric_test_shot(key: str):
    ''' Create a simple TestShot that just increments the cycles parameter `key` by 1, each time '''
    class CyclesNumericTestShot(TestShot):
        def next(self) -> bool:
            self.scene.cycles[key] += 1
            return True

        def back(self) -> None:
            self.scene.cycles[key] -= 1

    return CyclesNumericTestShot

def make_cycles_simple_bool_test_shot(key: str):
    ''' Create a simple TestShot that just sets the cycles parameter to `True`, once only '''
    class CyclesBoolTestShot(TestShot):
        def next(self) -> bool:
            # it can't get any truer than already True
            if self.scene.cycles[key]:
                return False

            self.scene.cycles[key] = True
            return True

        def back(self) -> None:
            self.scene.cycles[key] = False

    return CyclesBoolTestShot

def make_cycles_bounces_test_shot(key: str):
    ''' Create a TestShot that always guarantees adequate cycles `max_bounces` '''
    CyclesTestShot = make_cycles_simple_numeric_test_shot(key)
    class CyclesBouncesTestShot(CyclesTestShot):
        def ensure_total_bounces(self) -> None:
            # Transparent bounces are not needed here because they are handled separately
            self.scene.cycles.max_bounces = max(
                self.scene.cycles.diffuse_bounces,
                self.scene.cycles.glossy_bounces,
                self.scene.cycles.transmission_bounces,
                self.scene.cycles.volume_bounces,
            )

        def next(self) -> bool:
            result = super().next()
            self.ensure_total_bounces()
            return result

        def back(self) -> None:
            result = super().back()
            self.ensure_total_bounces()
            return result

    return CyclesBouncesTestShot

test_shots: Dict[Shot, Type[TestShot]] = {
    Shot.DIFFUSE: make_cycles_bounces_test_shot('diffuse_bounces'),
    Shot.GLOSSY: make_cycles_bounces_test_shot('glossy_bounces'),
    Shot.TRANSMISSION: make_cycles_bounces_test_shot('transmission_bounces'),
    Shot.TRANSPARENCY: make_cycles_simple_numeric_test_shot('transparent_max_bounces'),
    Shot.VOLUME: make_cycles_bounces_test_shot('volume_bounces'),
    Shot.CLAMP_INDIRECT: make_cycles_simple_numeric_test_shot('sample_clamp_indirect'),
    Shot.CAUSTIC_BLUR: make_cycles_simple_numeric_test_shot('blur_glossy'),
    Shot.CAUSTIC_REFLECTIVE: make_cycles_simple_bool_test_shot('caustics_reflective'),
    Shot.CAUSTIC_REFRACTIVE: make_cycles_simple_bool_test_shot('caustics_refractive'),
}


class SFR_OT_Render(Operator):
    shots: List[TestShot] = []
=======


class SFR_RenderFrame():
>>>>>>> Stashed changes
    stop: bool = False
    rendering: bool = False
    _timer: Timer = None

    def pre(self, dummy):
        self.rendering = True

    def post(self, dummy):
        self.rendering = False

    def cancelled(self, dummy):
        self.stop = True

    def execute(self, context):
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings
        status = settings.status # TODO: add property to track process status
        path = settings.inputdir

        self.stop = False
        self.rendering = False

        status.is_rendering = True
        status.should_stop = False

<<<<<<< Updated upstream
        # Construct each TestShot instance and give it access to the scene
        self.shots = list(test_shots[shot](scene) for shot in (
            Shot.DIFFUSE,
            Shot.GLOSSY,
            Shot.TRANSMISSION,
            Shot.GLOSSY,
            Shot.TRANSMISSION,
            Shot.TRANSPARENCY,
            Shot.VOLUME,
            Shot.CLAMP_INDIRECT,
            Shot.CAUSTIC_BLUR,
            Shot.CAUSTIC_REFLECTIVE,
            Shot.CAUSTIC_REFRACTIVE,
        ))

=======
>>>>>>> Stashed changes
        # Setup callbacks
        bpy.app.handlers.render_pre.append(self.render_pre)
        bpy.app.handlers.render_post.append(self.render_post)
        bpy.app.handlers.render_cancel.append(self.render_cancel)

<<<<<<< Updated upstream
        # Kick off the first iteration
=======
>>>>>>> Stashed changes
        render_frame(scene, path, 0)

        # Setup timer and modal
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)

    def modal(self, context, event):
        scene = context.scene
        settings: SFR_Settings = scene.sfr_settings
        status = settings.status
        path = settings.inputdir

        if event.type == 'TIMER':
            was_cancelled = self.stop or status.should_stop

            # If cancelled or no more shots to render, finish.
            if was_cancelled or not self.shots:

                # We remove the handlers and the modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                if was_cancelled:
                    self.report({'WARNING'}, "Benchmark aborted")
                    return {'CANCELLED'}

                self.report({'INFO'}, "Benchmark complete")
                return {"FINISHED"}

            elif self.rendering is False: 

                done_iteration = self.iteration
                next_iteration = done_iteration + 1

<<<<<<< Updated upstream
                shot: TestShot = self.shots[0]

                finish_shot = False
                if done_iteration > 0:
                    if compare(path, done_iteration, settings):
                        # there was no additional benefit from this setting change; roll it back.
                        shot.back()
                        # move onto next shot
                        finish_shot = True

                if not finish_shot:
                    # increment settings for next render
                    increment_setting_success = shot.next()

                    if not increment_setting_success:
                        # cannot increment setting anymore
                        # keep this setting, and move onto next shot
                        finish_shot = True

                if finish_shot:
                    self.shots.pop(0)
                    next_iteration = 0
=======
                if done_iteration > 0:
                    if compare(path, done_iteration, settings):
                        # reset; move onto next shot
                        self.shots.pop()
                        next_iteration = 0
>>>>>>> Stashed changes

                self.iteration = next_iteration

                # set off next render
                if self.shots:
                    render_frame(scene, path, next_iteration)


        return {"PASS_THROUGH"}

<<<<<<< Updated upstream

def get_filename(path: str, iteration: int) -> str:
    file_path = bpy.path.abspath(path)
    file_name = f"{str(iteration)}.png"
    return os.path.realpath(os.path.join(file_path, file_name))


def render_frame(scene, path, iteration):
    settings: SFR_Settings = scene.sfr_settings

    scene.render.filepath = get_filename(path, iteration)
=======
def render_frame(scene, path, iteration):
    settings: SFR_Settings = scene.sfr_settings

    # render first render
    scene.render.filepath = path + str(iteration) + ".png"
>>>>>>> Stashed changes
    scene.render.resolution_percentage = settings.resolution
    bpy.ops.render.render("INVOKE_DEFAULT", write_still = True)


<<<<<<< Updated upstream
def compare(path, iteration, settings):
    #Load first image
    BaseImage = io.imread(get_filename(path, iteration - 1))[:, :, :-1]
=======
def compare(path,iteration,settings):
        #Load first image
    BaseImage = io.imread(path + str(iteration - 1) + ".png")[:, :, :-1]
>>>>>>> Stashed changes
    #get first image data
    BI_Color = BaseImage.mean(axis=0).mean(axis=0)

    #Load second image
<<<<<<< Updated upstream
    SecondImage = io.imread(get_filename(path, iteration))[:, :, :-1]
=======
    SecondImage = io.imread(path + str(iteration) + ".png")[:, :, :-1]
>>>>>>> Stashed changes
    #get second image data
    SI_Color = SecondImage.mean(axis=0).mean(axis=0)

    ChangeThreshold = (settings.threshold/100)
    print(BI_Color)
    print(SI_Color)
    #get average
    BI_Brightness = BI_Color[0] + BI_Color[1] + BI_Color[2]
    SI_Brightness = SI_Color[0] + SI_Color[1] + SI_Color[2]
    #get brightness
    TI_Brightness = (SI_Brightness/BI_Brightness) - 1


    print(TI_Brightness)
    print("Threshold: ", settings.threshold, "%")

    if (SI_Brightness >= BI_Brightness) and (TI_Brightness >= ChangeThreshold):
        print("Finished Compare")
        return True

    else:
        print("Aborted Compare")
        return False