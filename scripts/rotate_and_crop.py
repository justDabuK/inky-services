from PIL import Image
from sys import argv

INKY_SCREEN_RESOLUTION = (600, 448)


def main():
    if len(argv) < 2:
        print('to less arguments, usage: ')
        print('rotate_and_crop.py <image>')
        exit(1)

    image_path = argv[1]
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    size = rotated_image.size
    box = (
        size[0]/2 - INKY_SCREEN_RESOLUTION[0]/2,
        size[1]/2 - INKY_SCREEN_RESOLUTION[1]/2,
        size[0]/2 + INKY_SCREEN_RESOLUTION[0]/2,
        size[1]/2 + INKY_SCREEN_RESOLUTION[1]/2
    )
    smaller_rotated_image = rotated_image.crop(box)
    image_name_split = image_path.split('.')
    smaller_rotated_image.save(image_name_split[0] + '_cropped_rotated.' + image_name_split[1])


if __name__ == "__main__":
    main()
