"""
This is an example that uses the MU3 Vision sensor to get video, and if it finds a face tells the bittle to walk forward. If not, to stand.
It is a proof of concept to use video stream from the MU3 with serial control of the bittle and a little computer vision.
"""

from datetime import datetime
import os
import time
from typing import Tuple

import cv2

from my_bittle.keyboard_listener import KeyboardListener
from my_bittle.bittle_serial_controller import BittleSerialController, BittleCommand
from my_mu3.mu3_image_grabber import Mu3ImageGrabber

IP_ADDRESS = "192.168.1.183"
SERIAL_PORT = "/dev/ttyS0"
SAVE_DIR = os.path.dirname(__file__)
FACE_CLASSIFIER = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
IMAGE_NAME_TEMPLATE = "frame_{}.png"
LATCH_TIME = 3


def find_face(image: "cv2.image") -> Tuple[bool, "cv2.image"]:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = FACE_CLASSIFIER.detectMultiScale(
        gray_image, minNeighbors=5, minSize=(20, 20)
    )
    face_found = False
    for (x, y, w, h) in face:
        face_found = True
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return face_found, image


def main():

    output_dir = os.path.join(
        SAVE_DIR, datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.mkdir(output_dir)

    my_bittle_controller = BittleSerialController(port=SERIAL_PORT)
    my_bittle_controller.start()

    my_mu3 = Mu3ImageGrabber(ip_address=IP_ADDRESS)
    my_mu3.start()

    my_keyboard_listener = KeyboardListener(key_timeout=0.01)

    frame_counter = 0
    exit_flag = False
    prev_cmd = BittleCommand.BALANCE
    last_cmd_time = 0
    start_time = time.time()

    while not exit_flag:

        image = my_mu3.get_image()
        if image is None:
            time.sleep(0.01)
            continue

        face_found, image = find_face(image)

        if face_found:
            cur_cmd = BittleCommand.FORWARD
        else:
            cur_cmd = BittleCommand.BALANCE

        if prev_cmd != cur_cmd and time.time() - last_cmd_time > LATCH_TIME:
            my_bittle_controller.command_bittle(cur_cmd)
            prev_cmd = cur_cmd
            last_cmd_time = time.time()
        frame_counter += 1
        cv2.imwrite(os.path.join(
            output_dir, IMAGE_NAME_TEMPLATE.format(frame_counter)), image)
        key = my_keyboard_listener.get_key()
        if key == "q":
            print("exiting")
            exit_flag = True
            end_time = time.time()

    my_bittle_controller.stop()
    my_mu3.stop()

    print(f"image processing fps: {frame_counter / (end_time - start_time)}")


if __name__ == "__main__":
    main()
