import bpy

import subprocess
import os

from .. import SFR_Settings

from skimage import io

def TestRender(path, iteration, settings: SFR_Settings):

    context = bpy.context
    scene = context.scene

    scene.render.resolution_percentage = settings.resolution

    if iteration == 0:
        # render first render
        scene.render.filepath = path + str(iteration) + ".png"
        bpy.ops.render.render(write_still=True)
        return True

    else:
        # render second render
        scene.render.filepath = path + str(iteration) + ".png"
        bpy.ops.render.render(write_still=True)

        # Load first image
        BaseImage = io.imread(
            path + str(iteration - 1) + ".png")[:, :, :-1]
        # get first image data
        BI_Color = BaseImage.mean(axis=0).mean(axis=0)

        # Load second image
        SecondImage = io.imread(path + str(iteration) + ".png")[:, :, :-1]
        # get second image data
        SI_Color = SecondImage.mean(axis=0).mean(axis=0)

        ChangeThreshold = (settings.threshold/100)
        #print(BI_Color)
        #print(SI_Color)
        # get average
        BI_Brightness = BI_Color[0] + BI_Color[1] + BI_Color[2]
        SI_Brightness = SI_Color[0] + SI_Color[1] + SI_Color[2]
        # get brightness
        TI_Brightness = (SI_Brightness/BI_Brightness) - 1

        #print(TI_Brightness)
        #print("Threshold: ", settings.threshold, "%")

        if (SI_Brightness >= BI_Brightness) and (TI_Brightness >= ChangeThreshold):
            print("Finished Compare")
            return True

        else:
            print("Aborted Compare")
            return False
