from os import listdir
from os.path import join, isfile
from sys import argv
from random import choice

def get_image_choice(image_dir):
    file_list = listdir(image_dir)
    image_list = []
    for file in file_list:
        file_path = join(image_dir, file)
        if isfile(file_path):
            image_list.append(file_path)

    return choice(image_list)

if __name__ == "__main__":
    if len(argv) < 2:
        print('to less arguments, usage: ')
        print('images_in_dir.py <image_directory>')
        exit(1)

    print(get_image_choice(argv[1]))
