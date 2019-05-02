import cv2
import numpy as np
from OpenCV_Processing.detectTshirtColors import extractShirtsColors
from OpenCV_Processing.AuxFunctions import calculateChangeColor
# from detectTshirtColors import extractShirtsColors
# from AuxFunctions import calculateChangeColor


def ChangeTshirtColors (img, lower_color_bounds1, upper_color_bounds1, transferColor1, lower_color_bounds2, upper_color_bounds2, transferColor2) :

    # Special Case Red Colour :
    # lower_color_bounds > upper_color_bounds1 then this is red colour
    # 2 ranges :  (0,upper_color_bounds)  (lower_color_bounds,180)

    # converting img to HSV
    frame = img
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    Red1 = False
    if lower_color_bounds1[0]>upper_color_bounds1[0]:
        Red1 = True
    Red2 = False
    if lower_color_bounds2[0]>upper_color_bounds2[0]:
        Red2 = True

    # Creating Transformation Matrices
    image_h, image_w, image_c = frame.shape
    transformationMatix1 = np.full((image_h, image_w, 3), transferColor1, dtype='uint8')
    transformationMatix2 = np.full((image_h, image_w, 3), transferColor2, dtype='uint8')
    modMatrix = np.full ((image_h, image_w), 180, dtype='uint8')
    # SVTransformationMatrix used to prevent S and V values to be more than 255
    SVTransformationMatrix = np.full ((image_h, image_w), 255, dtype='uint16')

    # Masking (extracting pixels of the color range from the img)
    # Detect an object based on the range of pixel values in the HSV colorspace.
    # special case for red handling, as red has 2 ranges
    if Red1:
        mask1 = cv2.inRange(frame_HSV, np.array([0, 40, 2]), upper_color_bounds1)
        mask_rgb1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2BGR)
        mask12 = cv2.inRange(frame_HSV, lower_color_bounds1, np.array([180, 255, 255]))
        mask_rgb12 = cv2.cvtColor(mask12, cv2.COLOR_GRAY2BGR)
    else:
        mask1 = cv2.inRange(frame_HSV, lower_color_bounds1, upper_color_bounds1)
        mask_rgb1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2BGR)
        #cv2.imshow("s", mask_rgb1)
        #cv2.waitKey()
    if Red2:
        mask2 = cv2.inRange(frame_HSV, np.array([0, 40, 2]), upper_color_bounds2)
        mask_rgb2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
        mask21 = cv2.inRange(frame_HSV, lower_color_bounds2, np.array([180, 255, 255]))
        mask_rgb21 = cv2.cvtColor(mask21, cv2.COLOR_GRAY2BGR)
    else:
        mask2 = cv2.inRange(frame_HSV,lower_color_bounds2, upper_color_bounds2)
        mask_rgb2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)

    maskedFrame1 = frame & mask_rgb1
    maskedFrame2 = frame & mask_rgb2
    if Red1:
        maskedFrame12 = frame & mask_rgb12
    if Red2:
        maskedFrame21 = frame & mask_rgb21   

    # Thresholding the mask to get mask of all 1s
    # Creating a mask of the transformation matrix values (will be added to original img to change color)
    ret1, thresholdedMask1 = cv2.threshold(maskedFrame1, 0, 255, cv2.THRESH_BINARY)
    ret2, thresholdedMask2 = cv2.threshold(maskedFrame2, 0, 255, cv2.THRESH_BINARY)
    if Red1:
        ret12, thresholdedMask12 = cv2.threshold(maskedFrame12, 0, 255, cv2.THRESH_BINARY)
    if Red2:
        ret21, thresholdedMask21 = cv2.threshold(maskedFrame21, 0, 255, cv2.THRESH_BINARY)

    maskedTransformationMatrix1 = thresholdedMask1 & transformationMatix1
    maskedTransformationMatrix2 = thresholdedMask2 & transformationMatix2
    if Red1:
        maskedTransformationMatrix12 = thresholdedMask12 & transformationMatix1
    if Red2:
        maskedTransformationMatrix21 = thresholdedMask21 & transformationMatix2    

    # Applying color transformation
    # Converting the frame to uint16 to avoid overflow when numbers are more than 255 due to addition
    frame_HSV = frame_HSV.astype(np.uint16)
    newFrame_HSV = (frame_HSV + maskedTransformationMatrix1)
    newFrame_HSV = (newFrame_HSV + maskedTransformationMatrix2)
    if Red1:
        newFrame_HSV = (newFrame_HSV + maskedTransformationMatrix12)
    if Red2:
        newFrame_HSV = (newFrame_HSV + maskedTransformationMatrix21)

    # performing modulo on H channel, to get numbers in range [0:180] only
    newFrame_HSV[:, :, 0] = np.remainder(newFrame_HSV[:, :, 0], modMatrix)
    # SVTransformationMatrix used to prevent S and V values to be more than 255
    newFrame_HSV[:, :, 1] = np.minimum(newFrame_HSV[:, :, 1], SVTransformationMatrix)
    newFrame_HSV[:, :, 2] = np.minimum(newFrame_HSV[:, :, 2], SVTransformationMatrix)

    # converting back to uint8
    newFrame_HSV = newFrame_HSV.astype(np.uint8)

    return cv2.cvtColor(newFrame_HSV, cv2.COLOR_HSV2BGR)


def main():

    img = cv2.imread('Test_Cases//redyellow2.png')
    # lower range, upper range and max pixels for each team
    l1, u1, m1, l2, u2, m2 = extractShirtsColors(img)

    # if the 2 detected ranges are the same, we will work on only one range
    if l1[0] == l2[0] and u1[0] == u2[0]:
        l2 = np.array([0, 0, 0])
        u2 = np.array([0, 0, 0])

    # choosing the 2 new colors for the teams
    color1 = calculateChangeColor([65, 0, 0], m1)
    color2 = calculateChangeColor([110, 0, 0], m2)

    recoloredFrame = ChangeTshirtColors(img, l1, u1, color1, l2, u2, color2)
    cv2.namedWindow("recolored frame", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
    recoloredFrames = cv2.resize(recoloredFrame, (960, 540))
    cv2.imshow("recolored frame", recoloredFrames)
    cv2.waitKey()

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
