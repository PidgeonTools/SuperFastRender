import bpy
from bpy.types import Context

from .. import SFR_Settings

def TestRender(path: str, iteration: int, settings: SFR_Settings):

    from skimage import io

    context: Context = bpy.context
    scene = context.scene

    scene.render.resolution_percentage = settings.resolution

    scene.render.filepath = path + str(iteration) + ".png"

    if iteration == 0:
        # render first render
        bpy.ops.render.render(write_still=True)
        return True

    else:
        # render second render
        bpy.ops.render.render(write_still=True)

        # Load first image
        BaseImage = io.imread(
            path + str(iteration - 1) + ".png")[:, :, :-1]
        # get first image average colour
        BI_Color = BaseImage.mean(axis=0).mean(axis=0)

        # Load second image
        SecondImage = io.imread(path + str(iteration) + ".png")[:, :, :-1]
        # get second image average colour
        SI_Color = SecondImage.mean(axis=0).mean(axis=0)

        #print(BI_Color)
        #print(SI_Color)
        # get brightness
        BI_Brightness = BI_Color[0] + BI_Color[1] + BI_Color[2]
        SI_Brightness = SI_Color[0] + SI_Color[1] + SI_Color[2]
        # calculate change in brightness
        TI_Brightness = (SI_Brightness/BI_Brightness) - 1 if BI_Brightness != 0 else 1

        #print(TI_Brightness)
        #print("Threshold: ", settings.threshold/100, "%")

        BaseImage = None
        SecondImage = None

        if (SI_Brightness >= BI_Brightness) and (TI_Brightness >= settings.threshold/100):
            print("Finished Compare")
            return True

        else:
            print("Aborted Compare")
            return False
