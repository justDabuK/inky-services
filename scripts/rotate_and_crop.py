from sys import argv

from inky_utility import rotate_and_crop_image


def main():
    if len(argv) < 2:
        print('to less arguments, usage: ')
        print('rotate_and_crop.py <image>')
        exit(1)

    image_path = argv[1]
    rotate_and_crop_image(image_path)


if __name__ == "__main__":
    main()
