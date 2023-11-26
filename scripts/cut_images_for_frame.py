from PIL import Image, ImageStat
from os import listdir

ORIGINAL_IMAGE_DIR = "../test_data/originals/"
ADJUSTED_IMAGE_DIR = "../test_data/adjusted/"

PORTRAIT_SIZES = (480, 800)
LANDSCAPE_SIZES = (800, 480)


def is_landscape(image):
    image_width = image.size[0]
    image_height = image.size[1]
    return image_width > image_height


def resize_image(image, size):
    image_width = image.size[0]
    image_height = image.size[1]
    # check which dimension is closest to goal size
    width_delta = abs(image_width - size[0])
    height_delta = abs(image_height - size[1])
    # calculate divider
    # TODO: should this be the smaller or larger delta?
    divider = size[1] / image_height if (width_delta > height_delta) else size[0] / image_width

    # resize using original size * divider
    resized_image = image.resize((int(image_width * divider), int(image_height * divider)))
    return resized_image


def crop_and_extend_image(original_image):
    inky_width = LANDSCAPE_SIZES[0]
    inky_height = LANDSCAPE_SIZES[1]
    image_width = original_image.size[0]
    image_height = original_image.size[1]

    smaller_width = min(inky_width, image_width)
    smaller_height = min(inky_height, image_height)
    box = (
        image_width / 2 - smaller_width / 2,
        image_height / 2 - smaller_height / 2,
        image_width / 2 + smaller_width / 2,
        image_height / 2 + smaller_height / 2
    )

    cropped_image = original_image.crop(box)

    median_color = ImageStat.Stat(cropped_image).median
    background_image = Image.new(cropped_image.mode, LANDSCAPE_SIZES, tuple(median_color))
    left_offset = int((inky_width - cropped_image.size[0]) / 2)
    top_offset = int((inky_height - cropped_image.size[1]) / 2)
    background_image.paste(cropped_image, (left_offset, top_offset))
    return background_image


def rotate_crop_and_extend_image(original_image):
    rotated_image = original_image.rotate(270, expand=True)
    return crop_and_extend_image(rotated_image)


def main():
    image_name_list = listdir(ORIGINAL_IMAGE_DIR)
    count = 0
    for image_name in image_name_list:
        if count % 10 == 0:
            print(f"{count}/{len(image_name_list)}")
        image = Image.open(ORIGINAL_IMAGE_DIR + image_name)

        if is_landscape(image):
            resized_image = resize_image(image, LANDSCAPE_SIZES)
            cropped_and_extend_image = crop_and_extend_image(resized_image)
        else:
            resized_image = resize_image(image, PORTRAIT_SIZES)
            cropped_and_extend_image = rotate_crop_and_extend_image(resized_image)
        # see if crop or padding is needed
        cropped_and_extend_image.save(ADJUSTED_IMAGE_DIR + image_name)
        count += 1


if __name__ == "__main__":
    main()
