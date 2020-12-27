from sys import argv

from inky_utility import rotate_and_resize


def main():
    if len(argv) < 2:
        print('to less arguments, usage: ')
        print('rotate_and_resize.py <image>')
        exit(1)

    image_path = argv[1]
    rotate_and_resize(image_path)


if __name__ == "__main__":
    main()
