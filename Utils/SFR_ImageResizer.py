
from skimage import data, color, io
from skimage.transform import resize
import os
nc = os.path.normcase
import pathlib

def resize_image(currFile, resizeFactor, path):
    if pathlib.Path(nc(path + currFile)).suffix == ".exr":
        print("Unspported file type, skipping " + currFile)
    else:
        image = io.imread(path + currFile)
        image_resized = resize(image, (image.shape[0] // resizeFactor + 1, image.shape[1] // resizeFactor + 1), anti_aliasing = True)
        io.imsave(path + currFile, image_resized, check_contrast=False)
        print("Successful optimization of " + currFile)