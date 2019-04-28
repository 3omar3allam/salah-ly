import numpy as np
import cv2


def apply_color_overlay(image,mask, intensity = 0.5,blue = 0, green = 0, red = 0):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_h, image_w, image_c = image.shape

    # creating matrix of same img dimensions and filling it with required color divided by 255
    color_bgra = (blue / 255, green / 255, red / 255)
    overlay = np.full((image_h, image_w, 3), color_bgra, dtype='float_')

    # converting the mask to desired color, and adding alpha channel initialized by ones
    tempMask = overlay*mask
    tempOnes = np.ones((image_h, image_w, 1))
    temp = np.concatenate((tempMask, tempOnes), axis=2)

    # overlaying the mask on the image
    cv2.addWeighted(np.uint8(temp), intensity, image, 1.0, 0, image)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    return image


def removeBackGround(frame, lower_color, higher_color):
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # extracting only the pitch
    mask = cv2.inRange(hsvFrame, lower_color, higher_color)
    maskedFrame = cv2.bitwise_and(hsvFrame, hsvFrame, mask=mask)

    # convert hsv to gray for thresholding
    maskedFrame_bgr = cv2.cvtColor(maskedFrame, cv2.COLOR_HSV2BGR)
    maskedFrame_gray = cv2.cvtColor(maskedFrame_bgr, cv2.COLOR_BGR2GRAY)

    # Performing closing to remove noise
    kernel = np.ones((10, 10), np.uint8)
    thresholdedMask = cv2.threshold(maskedFrame_gray, 0, 255, cv2.THRESH_BINARY)[1]
    thresholdedMask = cv2.morphologyEx(thresholdedMask, cv2.MORPH_CLOSE, kernel)

    # subtracting to get only the players without the background
    removedBackground = frame-cv2.bitwise_and(frame, frame, mask=thresholdedMask)

    return removedBackground


def imgHistogram (image, mask=None, maskFlag = 0, channelNo = 0):
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # if mask flag=1 and mask is none, the histogram will be for all the image
    # if flag=0, mask attribute will be the only parts of the image represented in the histogram
    if maskFlag != 1:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        thresholdedMask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)[1]
    else:
        thresholdedMask = mask

    # hist will be list of 255 elements, each carrying the no of pixels carrying this attribute
    # (H for example if cahnnelNo is 0)
    hist = cv2.calcHist([imageHSV], [channelNo], thresholdedMask, [256], [0, 256])
    return hist


def maxRangeFromHisto (H,maxIndexH,X):
    # starting at the maxIndex, and getting the range in the histogram
    # where the Y axis value is more than (curve average / percentageFromAverage)
    # endIndex = maxIndex
    # startIndex = maxIndex
    # Range = sum(hist) / (len(hist) * percentageFromAverage)

    # while True:
    #     endIndex = (endIndex + 1) % 256
    #     if endIndex == maxIndex:
    #         break
    #     if hist[endIndex] < Range:
    #         endIndex = (endIndex - 1) % 256
    #         break

    # while True:
    #     startIndex = (startIndex - 1) % 256
    #     if startIndex == maxIndex:
    #         break
    #     if hist[startIndex] < Range:
    #         startIndex = (startIndex + 1) % 256
    #         break
    startIndex=0
    endIndex=0
    if maxIndexH<=20:
        startIndex=0
        endIndex=20
    elif maxIndexH<=40 :
        startIndex=21
        endIndex=40
    elif maxIndexH<=80 :
        startIndex=41
        endIndex=80        
    elif maxIndexH<=95 :
        startIndex=81
        endIndex=95      
    elif maxIndexH<=140 :
        startIndex=96
        endIndex=140        
    elif maxIndexH<=170 :
        startIndex=141
        endIndex=170    
    elif maxIndexH<=180 :
        startIndex=171
        endIndex=180        

    return startIndex,endIndex                                                                                                              

    

