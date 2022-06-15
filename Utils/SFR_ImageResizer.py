from os.path import normcase
from pathlib import Path

def resize_image(currFile, resizeFactor, path):
    if Path(normcase(currFile)).suffix == ".exr":
        print("Unsupported file type, skipping " + currFile)
    else:
        from skimage import io
        from skimage.transform import resize

        # change output type to PNG
        out_file = str(Path(currFile).with_suffix(".png"))

        resizeFactor = pow(2, resizeFactor)
        image = io.imread(path + currFile)
        image_resized = resize(image, (image.shape[0] // resizeFactor, image.shape[1] // resizeFactor), anti_aliasing = True)
        io.imsave(path + out_file, image_resized, check_contrast=False)
        print("Successful optimization of " + currFile)
