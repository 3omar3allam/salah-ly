import numpy as np
import cv2
import matplotlib.pyplot as plt


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
    mask=cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # maskedFrame = cv2.bitwise_and(hsvFrame, hsvFrame, mask=mask)
    maskedFrame = frame & mask

    # convert hsv to gray for thresholding
    maskedFrame_gray = cv2.cvtColor(maskedFrame, cv2.COLOR_BGR2GRAY)

    # Performing closing to remove noise
    kernel = np.ones((10, 10), np.uint8)
    thresholdedMask = cv2.threshold(maskedFrame_gray, 0, 255, cv2.THRESH_BINARY)[1]
    thresholdedMask = cv2.morphologyEx(thresholdedMask, cv2.MORPH_CLOSE, kernel)
    thresholdedMask = cv2.cvtColor(thresholdedMask, cv2.COLOR_GRAY2BGR)

    # subtracting to get only the players without the background
    removedBackground = frame - (frame & thresholdedMask)

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
    if channelNo == 0:
        upperHistRange = 180
    else:
        upperHistRange = 256
    hist = cv2.calcHist([imageHSV], [channelNo], thresholdedMask, [upperHistRange], [0, upperHistRange])
    return hist


def maxRangeFromHisto (maxIndexH):
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

    # assigning every color to certain range according to hist max value
    startIndex = 0
    endIndex = 0
    if maxIndexH <= 19 or maxIndexH > 170:   # Red
        startIndex = 170
        endIndex = 19
    elif maxIndexH <= 31:                    # Yellow
        startIndex = 20
        endIndex = 31
    elif maxIndexH <= 60:                    # Greenstadium
        startIndex = 32
        endIndex = 60
    elif maxIndexH <= 88:                    # dark green
        startIndex = 61
        endIndex = 88
    elif maxIndexH <= 110:                   # light blue
        startIndex = 89
        endIndex = 110
    elif maxIndexH <= 169:                   # blue
        startIndex = 111
        endIndex = 169

    return startIndex, endIndex


def calculateChangeColor(color, originalColor):
    # this function is used to get the desired color to be added to original color, to get the new color chosen by user
    temp = color[0] - originalColor[0]
    # temp1=color[1]-originalColor[1]
    # temp2=color[2]-originalColor[2]
    return np.array([temp, 0, 0])

    

