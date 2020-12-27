from PIL import Image

INKY_SCREEN_RESOLUTION = (600, 448)


def set_image_and_show(inky, image_path, saturation=0.5):
    image = Image.open(image_path)
    inky.set_image(image, saturation=saturation)
    inky.show()


def rotate_and_crop_image(image_name, input_dir="", output_dir=""):
    image_path = input_dir + image_name
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    size = rotated_image.size
    box = (
        size[0] / 2 - INKY_SCREEN_RESOLUTION[0] / 2,
        size[1] / 2 - INKY_SCREEN_RESOLUTION[1] / 2,
        size[0] / 2 + INKY_SCREEN_RESOLUTION[0] / 2,
        size[1] / 2 + INKY_SCREEN_RESOLUTION[1] / 2
    )
    smaller_rotated_image = rotated_image.crop(box)
    image_name_split = image_name.split('.')
    output_path = output_dir + image_name_split[0] + '_cropped_rotated.' + image_name_split[1]
    smaller_rotated_image.save(output_path)
    return output_path
