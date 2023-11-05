from inky.auto import auto
from inky_utility import adjust_image
from inky_service import ADJUSTED_IMAGE_DIR, ORIGINAL_IMAGE_DIR
from os import listdir
from PIL import Image


def adjust_all_images():
    file_list = listdir(ORIGINAL_IMAGE_DIR)
    count = 0
    for file in file_list:
        if count % 10 == 0:
            print(f"{count}/{len(file_list)}")
        adjust_image(file, ORIGINAL_IMAGE_DIR, ADJUSTED_IMAGE_DIR)
        count += 1


def find_mixed_files():
    inky = auto()
    inky_width = inky.resolution[1]
    inky_height = inky.resolution[0]
    file_list = listdir(ORIGINAL_IMAGE_DIR)
    count = 0
    count_greater = 0
    count_lesser = 1
    mixed_files = []
    for file in file_list:
        if count % 10 == 0:
            print(f"{count}/{len(file_list)}")
        image_path = ORIGINAL_IMAGE_DIR + file
        image = Image.open(image_path)
        image_width = image.size[0]
        image_height = image.size[1]

        if image_width >= inky_width and image_height >= inky_height:
            count_greater += 1
        elif image_width <= inky_width and image_height <= inky_height:
            count_lesser += 1
        else:
            mixed_files.append(file)
        count += 1

    print(f"greater then {count_greater}")
    print(f"lesser then {count_lesser}")
    print(f"mixed files({len(mixed_files)}):")
    print(mixed_files)


def main():
    adjust_all_images()


if __name__ == "__main__":
    main()
