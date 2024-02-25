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

    picture_dir = sys.argv[1]
    choice = get_image_choice(f"{picture_dir}/originals")
    file_ending = choice.split(".")[-1]

    print(f"going to set {choice} as the current image")

    shutil.copy(choice, f"{picture_dir}/current/current.{file_ending}")


