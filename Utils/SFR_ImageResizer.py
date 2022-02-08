import os
nc = os.path.normcase
import pathlib

def resize_image(currFile, resizeFactor, path):
    if pathlib.Path(nc(path + currFile)).suffix == ".exr":
        print("Unsupported file type, skipping " + currFile)
    else:
        from skimage import io
        from skimage.transform import resize

        resizeFactor = pow(2, resizeFactor)
        image = io.imread(path + currFile)
        image_resized = resize(image, (image.shape[0] // resizeFactor, image.shape[1] // resizeFactor), anti_aliasing = True)
        io.imsave(path + currFile, image_resized, check_contrast=False)
        print("Successful optimization of " + currFile)
