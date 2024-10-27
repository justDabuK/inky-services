import requests
import shutil
from PIL import Image
from inky.auto import auto

inky = auto()

if __name__ == "__main__":
    url = "http://192.168.178.29:8000/images/current/get/download"

    response = requests.put(url, json=inky.resolution, stream=True)
    file_ending = response.headers['content-disposition'].split(';')[1].split('.')[-1].replace('"', '')
    current_image_path = f"/home/pi/current_image.{file_ending}"

    with open(current_image_path, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    current_image = Image.open(current_image_path)
    inky.set_image(current_image)
    inky.show()
