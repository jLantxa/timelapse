#!/usr/bin/env python3

import cv2
import time
import sys
import subprocess

from timeit import default_timer as timer

class Timelapse():
    def __init__(self, interval):
        self.interval = interval

    def run(self):
        n = 0
        start = timer()
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 1920)
        self.camera.set(4, 1080)

        while True:
            start = timer()
            s, img = self.camera.read()
            if s:
                cv2.imwrite("pic" + str(n) + ".jpg", img)
                n += 1
                print(f"Frame {n}")

            now = timer()
            remaining = self.interval - (now - start)
            if (remaining > 0):
                time.sleep(remaining)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Error: Specify an interval for the timelapse")
        exit()

    interval = float(sys.argv[1])
    timelapse_camera = Timelapse(interval)
    timelapse_camera.run()
