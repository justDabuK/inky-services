#!/usr/bin/env python3
import sys
from inky.inky_uc8159 import Inky
from images_in_dir import get_image_choice
from inky_utility import set_image_and_show

inky = Inky()

if len(sys.argv) == 1:
    print("""
Usage: {file} image-directory
""".format(file=sys.argv[0]))
    sys.exit(1)

choice = get_image_choice(sys.argv[1])
print("going to set " + choice)
set_image_and_show(inky, choice)
