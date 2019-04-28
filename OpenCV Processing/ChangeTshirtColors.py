import cv2
import numpy as np
# from detectTshirtColors import extractShirtsColors



def ChangeTshirtColors (img, lower_color_bounds1, upper_color_bounds1, transferColor1, lower_color_bounds2, upper_color_bounds2, transferColor2) :

    #Special Case Red Colour :
    #                   lower_color_bounds>upper_color_bounds1 then this is red colour 
    #         2 ranges :  (0,upper_color_bounds)  (lower_color_bounds,180)
    # converting img to HSV
    frame = img
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    Red1=False 
    if lower_color_bounds1[0]>upper_color_bounds1[0] :
        Red1=True
    Red2=False    
    if lower_color_bounds2[0]>upper_color_bounds2[0] :
        Red2=True

    # Creating Transformation Matrices
    image_h, image_w, image_c = frame.shape
    transformationMatix1 = np.full((image_h, image_w, 3), transferColor1, dtype='uint8')
    transformationMatix2 = np.full((image_h, image_w, 3), transferColor2, dtype='uint8')
    # Masking (extracting pixels of the color range from the img)
    if Red1:
        mask1 = cv2.inRange(frame_HSV,(0,40,2), upper_color_bounds1)  # Detect an object based on the range of pixel values in the HSV colorspace.
        mask_rgb1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2BGR)
        mask12 = cv2.inRange(frame_HSV, lower_color_bounds1, (180,255,255))  # Detect an object based on the range of pixel values in the HSV colorspace.
        mask_rgb12 = cv2.cvtColor(mask12, cv2.COLOR_GRAY2BGR)        
    else :
        mask1 = cv2.inRange(frame_HSV, lower_color_bounds1, upper_color_bounds1)  # Detect an object based on the range of pixel values in the HSV colorspace.
        mask_rgb1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2BGR)
    if Red2 :
        mask2 = cv2.inRange(frame_HSV, (0,40,2), upper_color_bounds2)  # Detect an object based on the range of pixel values in the HSV colorspace.
        mask_rgb2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
        mask21 = cv2.inRange(frame_HSV, lower_color_bounds1, (180,255,255))  # Detect an object based on the range of pixel values in the HSV colorspace.
        mask_rgb21= cv2.cvtColor(mask21, cv2.COLOR_GRAY2BGR)   
    else :
        mask2 = cv2.inRange(frame_HSV,lower_color_bounds2, upper_color_bounds2)  # Detect an object based on the range of pixel values in the HSV colorspace.
        mask_rgb2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
        cv2.imshow("mask_rgb2", mask_rgb2)          
            
    # cv2.imshow("Mssk RGB  ", mask_rgb)
    maskedFrame1 = frame & mask_rgb1
    maskedFrame2 = frame & mask_rgb2
    if Red1:
        maskedFrame12 = frame & mask_rgb12
    if Red2 :
        maskedFrame21 = frame & mask_rgb21   
        cv2.imshow("maskedFrame2",maskedFrame2)


    # Thresholding the mask to get mask of all 1s
    ret1, thresholdedMask1 = cv2.threshold(maskedFrame1, 0, 255, cv2.THRESH_BINARY)
    ret2, thresholdedMask2 = cv2.threshold(maskedFrame2, 0, 255, cv2.THRESH_BINARY)
    if Red1:
        ret12, thresholdedMask12 = cv2.threshold(maskedFrame12, 0, 255, cv2.THRESH_BINARY)
    if Red2 :
        ret21, thresholdedMask21 = cv2.threshold(maskedFrame21, 0, 255, cv2.THRESH_BINARY)    # Creating a mask of the transformation matrix values (will be added to original img to change color)
    maskedTransformationMatrix1 = thresholdedMask1 & transformationMatix1
    maskedTransformationMatrix2 = thresholdedMask2 & transformationMatix2
    if Red1:
        maskedTransformationMatrix12 = thresholdedMask12 & transformationMatix1
    if Red2 :
        maskedTransformationMatrix21 = thresholdedMask21 & transformationMatix2    


    # Applying color transformation
    newFrame_HSV = (frame_HSV + maskedTransformationMatrix1)
    newFrame_HSV = (newFrame_HSV + maskedTransformationMatrix2)
    if Red1:
        newFrame_HSV = (newFrame_HSV + maskedTransformationMatrix12)
    if Red2 :
        newFrame_HSV = (newFrame_HSV + maskedTransformationMatrix21)
    return cv2.cvtColor(newFrame_HSV, cv2.COLOR_HSV2BGR)


def main():

    img = cv2.imread('Test_Cases//Orange.png')
    # red
    lower_color_bounds1 = (165,40,0)
    upper_color_bounds1 = (19,255,255)
    # blue
    lower_color_bounds2 = (110,40,0)
    upper_color_bounds2 = (170,255,255)
    # green
    # lower_color_bounds = (35, 50, 40 )
    # upper_color_bounds = (55, 255, 255)
    recoloredFrame = ChangeTshirtColors(img, lower_color_bounds1, upper_color_bounds1, (50, 0,0),lower_color_bounds2, upper_color_bounds2, (130, -30, -30)) # (100,0,0) is the value added to the red pixels
    cv2.namedWindow("recolored frame", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
    recoloredFrames = cv2.resize(recoloredFrame, (960, 540))
    cv2.imshow("recolored frame", recoloredFrames)
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
