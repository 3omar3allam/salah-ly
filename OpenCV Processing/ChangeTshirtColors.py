import cv2
import numpy as np
from AuxFunctions import apply_color_overlay

def ChangeTshirtColors(img, lower_color_bounds, upper_color_bounds):
    frame = img
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_HSV, lower_color_bounds, upper_color_bounds)
    # mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((1, 3), np.uint8))
    # mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((1, 3), np.uint8))

    # cv2.imshow('ReColored Frame', mask)
    # cv2.waitKey()
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    frame = frame & mask_rgb
    cv2.imshow('ReColored Frame', frame)
    cv2.waitKey()
    ret, thresh1 = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY)

    cv2.imshow('ReColored Frame', thresh1)
    cv2.waitKey()

    reColoredFrame = apply_color_overlay(img, thresh1, 1, 0, 255, 255)
    return  reColoredFrame


def main():
    img = cv2.imread('IPTest.jpg')
    lower_color_bounds = (0,120,70)
    upper_color_bounds = (10,255,255)

    reColoredFrame = ChangeTshirtColors(img, lower_color_bounds, upper_color_bounds)

    cv2.imshow('ReColored Frame', reColoredFrame)
    cv2.waitKey()


if __name__ =="__main__":
    main()

