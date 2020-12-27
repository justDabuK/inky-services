#!/usr/bin/env python3

import sys

from PIL import Image
from inky.inky_uc8159 import Inky
from images_in_dir import get_image_choice

inky = Inky()
saturation = 0.5

if len(sys.argv) == 1:
    print("""
Usage: {file} image-directory
""".format(file=sys.argv[0]))
    sys.exit(1)

choice = get_image_choice(sys.argv[1])
print("going to set " + choice)
image = Image.open(choice)

if len(sys.argv) > 2:
    saturation = float(sys.argv[2])

inky.set_image(image, saturation=saturation)
inky.show()
