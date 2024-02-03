from PIL import Image, ImageStat
from inky.auto import auto

display = auto()
INKY_SCREEN_RESOLUTION = display.resolution


def set_image_from_path_and_show(inky, image_path, saturation=0.5):
    image = adjust_image(image_path)
    inky.set_image(image, saturation=saturation)
    inky.show()


def rotate_and_crop_image(image_path):
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    size = rotated_image.size
    box = (
        size[0] / 2 - INKY_SCREEN_RESOLUTION[0] / 2,
        size[1] / 2 - INKY_SCREEN_RESOLUTION[1] / 2,
        size[0] / 2 + INKY_SCREEN_RESOLUTION[0] / 2,
        size[1] / 2 + INKY_SCREEN_RESOLUTION[1] / 2
    )

    return rotated_image.crop(box)


def rotate_and_extend_image(image_path):
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    median_color = ImageStat.Stat(original_image).median

    background_image = Image.new(rotated_image.mode, INKY_SCREEN_RESOLUTION, tuple(median_color))
    left_offset = int((INKY_SCREEN_RESOLUTION[0] - rotated_image.size[0]) / 2)
    top_offset = int((INKY_SCREEN_RESOLUTION[1] - rotated_image.size[1]) / 2)
    background_image.paste(rotated_image, (left_offset, top_offset))

    return background_image


def rotate_crop_and_extend_image(image_path):
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)
    inky_width = INKY_SCREEN_RESOLUTION[0]
    inky_height = INKY_SCREEN_RESOLUTION[1]
    image_width = rotated_image.size[0]
    image_height = rotated_image.size[1]

    smaller_width = min(inky_width, image_width)
    smaller_height = min(inky_height, image_height)
    box = (
        image_width / 2 - smaller_width / 2,
        image_height / 2 - smaller_height / 2,
        image_width / 2 + smaller_width / 2,
        image_height / 2 + smaller_height / 2
    )

    cropped_rotated_image = rotated_image.crop(box)

    median_color = ImageStat.Stat(cropped_rotated_image).median
    background_image = Image.new(cropped_rotated_image.mode, INKY_SCREEN_RESOLUTION, tuple(median_color))
    left_offset = int((inky_width - cropped_rotated_image.size[0]) / 2)
    top_offset = int((inky_height - cropped_rotated_image.size[1]) / 2)
    background_image.paste(cropped_rotated_image, (left_offset, top_offset))

    return background_image


def adjust_image(image_path):
    inky_width = INKY_SCREEN_RESOLUTION[0]
    inky_height = INKY_SCREEN_RESOLUTION[1]

    image = Image.open(image_path)
    image_width = image.size[0]
    image_height = image.size[1]

    if image_width >= inky_width and image_height >= inky_height:
        return rotate_and_crop_image(image_path)
    elif image_width <= inky_width and image_height <= inky_height:
        return rotate_and_extend_image(image_path)
    else:
        return rotate_crop_and_extend_image(image_path)


def rotate_and_resize(image_path):
    original_image = Image.open(image_path)
    rotated_image = original_image.rotate(270, expand=True)

    return rotated_image.resize(INKY_SCREEN_RESOLUTION)
