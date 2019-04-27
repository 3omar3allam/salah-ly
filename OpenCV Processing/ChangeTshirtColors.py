import cv2
import numpy as np
# from detectTshirtColors import extractShirtsColors



def ChangeTshirtColors (img, lower_color_bounds1, upper_color_bounds1, transferColor1, lower_color_bounds2, upper_color_bounds2, transferColor2) :

    # converting img to HSV
    frame = img
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Creating Transformation Matrices
    image_h, image_w, image_c = frame.shape
    transformationMatix1 = np.full((image_h, image_w, 3), transferColor1, dtype='uint8')
    transformationMatix2 = np.full((image_h, image_w, 3), transferColor2, dtype='uint8')

    # Masking (extracting pixels of the color range from the img)
    mask1 = cv2.inRange(frame_HSV, lower_color_bounds1, upper_color_bounds1)  # Detect an object based on the range of pixel values in the HSV colorspace.
    mask_rgb1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2BGR)
    mask2 = cv2.inRange(frame_HSV, lower_color_bounds2, upper_color_bounds2)  # Detect an object based on the range of pixel values in the HSV colorspace.
    mask_rgb2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
    cv2.imshow("mask_rgb2", mask_rgb2)



    # cv2.imshow("Mssk RGB  ", mask_rgb)
    maskedFrame1 = frame & mask_rgb1
    maskedFrame2 = frame & mask_rgb2
    cv2.imshow("maskedFrame2",maskedFrame2)


    # Thresholding the mask to get mask of all 1s
    ret1, thresholdedMask1 = cv2.threshold(maskedFrame1, 0, 255, cv2.THRESH_BINARY)
    ret2, thresholdedMask2 = cv2.threshold(maskedFrame2, 0, 255, cv2.THRESH_BINARY)

    # Creating a mask of the transformation matrix values (will be added to original img to change color)
    maskedTransformationMatrix1 = thresholdedMask1 & transformationMatix1
    maskedTransformationMatrix2 = thresholdedMask2 & transformationMatix2
    cv2.imshow("maskedTransformationMatrix2", maskedTransformationMatrix2)


    # Applying color transformation
    newFrame_HSV = frame_HSV + maskedTransformationMatrix1
    newFrame_HSV = newFrame_HSV + maskedTransformationMatrix2

    return cv2.cvtColor(newFrame_HSV, cv2.COLOR_HSV2BGR)


def main():

    img = cv2.imread('Senegal-VS-Colombia.jpg')
    # red
    lower_color_bounds1 = (0,120,70)
    upper_color_bounds1 = (16,255,255)
    # blue
    lower_color_bounds2 = (70,0,0)
    upper_color_bounds2 = (120,255,255)
    # green
    # lower_color_bounds = (35, 50, 40 )
    # upper_color_bounds = (55, 255, 255)
    recoloredFrame = ChangeTshirtColors(img, lower_color_bounds1, upper_color_bounds1, (100, 0, 0),lower_color_bounds2, upper_color_bounds2, (-70, 0, 0)) # (100,0,0) is the value added to the red pixels
    cv2.imshow("recolored frame", recoloredFrame)
    cv2.waitKey()


    # testing change color after extracting colors from the image
    # l1,u1,l2,u2 = extractShirtsColors(img)
    # reColoredFrame2 = ChangeTshirtColors(img, l2, u2, (-75, 30, -70))
    # cv2.imshow('reColoredFrame', reColoredFrame2)
    # cv2.waitKey()
    # reColoredFrame1 = ChangeTshirtColors(reColoredFrame2, l1, u1, (100, 0, 0))
    # cv2.imshow('reColoredFrame', reColoredFrame1)
    # cv2.waitKey()

if __name__ == "__main__":
    main()



    # ----------------------------------------------------------------------------- morphological operations trials here -----------------------------------------------------
    # kernel = np.ones((10, 3), np.uint8)
    # # thresh = cv2.threshold(res_gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cleanMask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("cleanMask  ", cleanMask)
    # cv2.waitKey()
    # # mask = cleanMask
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
