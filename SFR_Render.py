import subprocess
import os
import bpy

from . import SFR_Settings

from bpy.types import (
    Operator
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





class SFR_OT_Render(Operator):
    def pre(self, dummy):
        self.rendering = True

    def post(self, dummy):
        self.shots.pop(0)
        self.rendering = False

    def cancelled(self, dummy):
        self.stop = True

    def execute(self, context):
        scene = context.scene

        self.stop = False
        self.rendering = False

        status.is_rendering = True
        status.should_stop = False

        # Setup callbacks
        bpy.app.handlers.render_pre.append(self.render_pre)
        bpy.app.handlers.render_post.append(self.render_post)
        bpy.app.handlers.render_cancel.append(self.render_cancel)

        # Setup timer and modal
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)

    def modal(self, context, event,path,iteration,settings):
        if event.type == 'TIMER': 

            # If cancelled or no more shots to render, finish.
            if True in (not self.shots, self.stop is True): 

                # We remove the handlers and the modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                return {"FINISHED"}

            elif self.rendering is False: 
                        
                context = bpy.context
                scene = context.scene
                
                scene.render.resolution_percentage = settings.resolution

                render_frame(path, iteration)
                if iteration > 0:
                    compare(path,iteration,settings)
                    return True


        return {"PASS_THROUGH"}

def render_frame(path, iteration):
    # render first render
    scene.render.filepath = path + str(iteration) + ".png"
    bpy.ops.render.render("INVOKE_DEFAULT", write_still = True)


def compare(path,iteration,settings):
        #Load first image
    BaseImage = io.imread(path + str(iteration - 1) + ".png")[:, :, :-1]
    #get first image data
    BI_Color = BaseImage.mean(axis=0).mean(axis=0)

    #Load second image
    SecondImage = io.imread(path + str(iteration) + ".png")[:, :, :-1]
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