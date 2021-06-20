#!/usr/bin/env python3

"""
Timelapse capturer
"""

import argparse
import time

from timeit import default_timer as timer

import cv2

def run_timelapse(interval):
    """ Run timelapse """

    frame_num = 0
    time_start = timer()
    camera = cv2.VideoCapture(0)
    camera.set(3, 1920)
    camera.set(4, 1080)

    while True:
        time_start = timer()
        read_ok, frame = camera.read()
        if read_ok:
            cv2.imwrite("pic" + str(frame_num) + ".jpg", frame)
            frame_num += 1
            print(f"Frame {frame_num}")

        time_now = timer()
        remaining = interval - (time_now - time_start)
        if remaining > 0:
            time.sleep(remaining)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Timelapse capturer.')
    parser.add_argument('interval', type=float, help='The interframe time interval in seconds')
    args = parser.parse_args()

    run_timelapse(args.interval)
