#!/usr/bin/env python3

import argparse
import datetime
import logging
import os
import picamera2
from PIL import Image
from threading import Thread
import time

MIN_INTERVAL = 1.0

class TimelapseCamera():
    def __init__(self):
        self.running = False
        self.picam2 = picamera2.Picamera2()
        self.config = self.picam2.still_configuration()
        self.picam2.configure(self.config)
        self.picam2.start()

    def __deinit__(self):
        self.picam2.stop()

    def __write_image(self, array, filename):
        im = Image.fromarray(array)
        im.save(filename)

    def __run(self, path: str, interval: float, num_pictures: int):
        if interval < MIN_INTERVAL:
            logging.warn("Adjusted interval to {MIN_INTERVAL} s.")
            interval = MIN_INTERVAL

        date = datetime.datetime.now()
        datestr = f"{date.year}{date.month:02}{date.day:02}_{date.hour:02}{date.minute:02}{date.second:02}"
        capture_path = f"{path}/{datestr}"

        os.makedirs(capture_path)
        logging.info(f"Saving capture in {capture_path}/")

        logging.info("Starting...")

        i = 0
        self.running = True
        while self.running:
            start = datetime.datetime.now()

            array = self.picam2.capture_array()
            filename = f"{capture_path}/capture_{i}.jpg"
            write_thread = Thread(target=self.__write_image, args=(array, filename))
            write_thread.start()

            i += 1
            if (num_pictures > 0) and (i >= num_pictures):
                self.running = False
                break

            end = datetime.datetime.now()
            delta = (end - start).total_seconds()
            sleep_time = (interval - delta)
            time.sleep(sleep_time)

    def start(self, path: str, interval: float, num_pictures: int, wait=True):
        if wait == True:
            self.__run(path, interval, num_pictures)
        else:
            thread = Thread(target=self.__run, args=(path, interval, num_pictures))
            thread.start()

    def stop(self):
        self.running = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Timelapse camera utility")
    parser.add_argument("-p", "--path", type=str, default=".", help="Path to save captured images.")
    parser.add_argument("-i", "--interval", type=float, required=True, help="Interval between captures.")
    parser.add_argument("-n", "--num_pictures", type=int, default=0, help="Number of images to capture.")
    args = parser.parse_args()

    timelapse_camera = TimelapseCamera()
    timelapse_camera.start(args.path, args.interval, args.num_pictures)

