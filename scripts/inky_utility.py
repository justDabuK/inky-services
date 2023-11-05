from PIL import Image, ImageStat
from inky.auto import auto

display = auto()
INKY_SCREEN_RESOLUTION = display.resolution


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


def rotate_and_extend_image(image_name, input_dir="", output_dir=""):
    image_path = input_dir + image_name
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    median_color = ImageStat.Stat(original_image).median

    background_image = Image.new(rotated_image.mode, INKY_SCREEN_RESOLUTION, tuple(median_color))
    left_offset = int((INKY_SCREEN_RESOLUTION[0] - rotated_image.size[0]) / 2)
    top_offset = int((INKY_SCREEN_RESOLUTION[1] - rotated_image.size[1]) / 2)
    background_image.paste(rotated_image, (left_offset, top_offset))

    image_name_split = image_name.split('.')
    output_path = output_dir + image_name_split[0] + '_extended_rotated.' + image_name_split[1]
    background_image.save(output_path)

    return output_path


def rotate_and_resize(image_name, input_dir="", output_dir=""):
    image_path = input_dir + image_name
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    smaller_rotated_image = rotated_image.resize(INKY_SCREEN_RESOLUTION)
    image_name_split = image_path.split('.')
    output_path = output_dir + image_name_split[0] + '_resized_rotated.' + image_name_split[1]
    smaller_rotated_image.save(output_path)
    return output_path
