import cv2
import numpy as np


def ChangeTshirtColors (img, lower_color_bounds, upper_color_bounds) :

    # converting img to HSV
    frame = img
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Creating Transformation Matrices
    image_h, image_w, image_c = frame.shape
    transformationMatix = np.full((image_h, image_w, 3), (10, 0, 0), dtype='uint8')
    modMatrix = np.full((image_h, image_w, 3), (255, 255, 255), dtype='uint8')

    # Masking (extracting pixels of the color range from the img)
    mask = cv2.inRange(frame_HSV, lower_color_bounds, upper_color_bounds)
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    maskedFrame = frame & mask_rgb

    # Thresholding the mask to get mask of all 1s
    ret, thresholdedMask = cv2.threshold(maskedFrame, 0, 255, cv2.THRESH_BINARY)
    # Creating a mask of the transformation matrix values (will be added to original img to change color)
    maskedTransformationMatrix = thresholdedMask & transformationMatix

    # Applying color transformation
    newFrame_HSV = frame_HSV - maskedTransformationMatrix

    return cv2.cvtColor(newFrame_HSV, cv2.COLOR_HSV2BGR)


def main():
    img = cv2.imread('IPTest.jpg')
    lower_color_bounds = (0,120,70)
    upper_color_bounds = (10,255,255)
    # lower_color_bounds = (50, 50, 40 )
    # upper_color_bounds = (100, 255, 255)

    reColoredFrame = ChangeTshirtColors(img, lower_color_bounds, upper_color_bounds)
    cv2.imshow('reColoredFrame', reColoredFrame)
    cv2.waitKey()

if __name__ =="__main__":
    main()