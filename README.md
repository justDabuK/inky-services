# Inky
Scripts to control [Inky Impression](https://shop.pimoroni.com/products/inky-impression), a 7 color ePaper.

These instructions are written for a raspberry pi.

# Requirements
If pi Zero W, then one first need to set up Wifi on another Pi.
And before that, allowing SSH by putting a file with the name `SSH` into the root directory of the SD-Card.
Python 3 should be pre installed.

Required installations on the running pi: 
- [Pimoroni-Inky](https://github.com/pimoroni/inky) for the controlling the screen
- [FastAPI](https://fastapi.tiangolo.com/) for the service-endpoints
- [Uvicorn](https://www.uvicorn.org/) to run the server offering the endpoints
- [Python-Multipart](https://pypi.org/project/python-multipart/) to be able to handle files sended to the endpoints


    curl https://get.pimoroni.com/inky | bash
    pip3 install fastapi
    pip3 install uvicorn
    pip3 install python-multipart

# Install
prepare the `DaBu` directory and clone this repo into the directory

    mkdir ~/DaBu
    cd ~/DaBu
    git clone https://github.com/justDabuK/inky.git

Prepare further directories to ensure the correct functioning of the inky-service

    mkdir ~/logs
    mkdir ~/Pictures/originals
    mkdir ~/Pictures/adjusted

# cronjobs
To make the `inky_service` start at reboot and to make the screen switch the image every hour one can add this commands as cronjobs. First type

    crontab -e

Then add these two lines at the end of the file.

    @reboot /home/pi/.local/bin/uvicorn --app-dir /home/pi/DaBu/inky/scripts --host 0.0.0.0 inky_service:app > /home/pi/logs/inky_service.logs 2>&1
    0 *  *   *   *     python3 /home/pi/DaBu/inky/scripts/set_random_image.py /home/pi/Pictures/adjusted/
