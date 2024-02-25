import os
import sys
import shutil
from images_in_dir import get_image_choice

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""
    Usage: {file} picture-directory
    
    where image-directory contains the originals and the current folder
    """.format(file=sys.argv[0]))
        sys.exit(1)

    # setup directory paths
    picture_dir = sys.argv[1]
    originals_dir = f"{picture_dir}/originals"
    current_dir = f"{picture_dir}/current"

    # clean current directory
    shutil.rmtree(current_dir)
    os.mkdir(current_dir)

    # choose a new image and copy it into the current folder
    choice = get_image_choice(originals_dir)
    file_ending = choice.split(".")[-1]
    print(f"going to set {choice} as the current image")
    shutil.copy(choice, f"{picture_dir}/current/current.{file_ending}")


