#!/usr/bin/env python3
import sys
from inky.auto import auto
from images_in_dir import get_image_choice
from inky_utility import set_image_from_path_and_show

inky = auto()

if len(sys.argv) == 1:
    print("""
Usage: {file} image-directory
""".format(file=sys.argv[0]))
    sys.exit(1)

input_dir = sys.argv[1]
choice = get_image_choice(input_dir)
print("going to set " + choice)
set_image_from_path_and_show(inky, choice)
