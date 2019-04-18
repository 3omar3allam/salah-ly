import cv2
from AuxFunctions import apply_color_overlay

def ChangeTshirtColors(img, lower_color_bounds, upper_color_bounds):
    frame = img
    mask = cv2.inRange(frame, lower_color_bounds, upper_color_bounds)
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    frame = frame & mask_rgb
    ret, thresh1 = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY)
    reColoredFrame = apply_color_overlay(img, thresh1, 1, 0, 255, 255)
    return  reColoredFrame


def main():
    img = cv2.imread('IPTest.jpg')
    lower_color_bounds = (40, 0, 0)
    upper_color_bounds = (225, 90, 90)

    reColoredFrame = ChangeTshirtColors(img, lower_color_bounds, upper_color_bounds)

    cv2.imshow('ReColored Frame', reColoredFrame)
    cv2.waitKey()


if __name__ =="__main__":
    main()

