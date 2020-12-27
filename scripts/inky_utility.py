from PIL import Image


def set_image_and_show(inky, image_path, saturation=0.5):
    image = Image.open(image_path)
    inky.set_image(image, saturation=saturation)
    inky.show()
