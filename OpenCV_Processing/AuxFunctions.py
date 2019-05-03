import numpy as np
import cv2


def removeBackGround(frame, lower_color, higher_color):
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # extracting only the pitch
    mask = cv2.inRange(hsvFrame, lower_color, higher_color)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
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
    # assigning every color to certain range according to hist max value
    startIndex = 0
    endIndex = 0
    if maxIndexH <= 19 or maxIndexH > 170:   # Red
        startIndex = 170
        endIndex = 19
    elif maxIndexH <= 31:                    # Yellow
        startIndex = 20
        endIndex = 31
    elif maxIndexH <= 60:                    # Green stadium
        startIndex = 32
        endIndex = 60
    elif maxIndexH <= 88:                    # dark green
        startIndex = 61
        endIndex = 88
    # elif maxIndexH <= 103:                 # light blue
    #     startIndex = 89
    #     endIndex = 103
    elif maxIndexH <= 169:                   # blue
        startIndex = 104
        endIndex = 169

    return startIndex, endIndex


def calculateChangeColor(newColor, originalColor):
    # this function is used to get the desired color to be added to original color, to get the new color chosen by user

    # detecting if the color dark blue
    blue = False
    darkblue = False
    if 105 <= originalColor[0] <= 168:
        blue = True
    if blue and originalColor[0] > 119:
        darkblue = True
    if blue and originalColor[1] > 35:
        darkblue = True

    temp = np.mod((newColor[0] - originalColor[0]), 180)

    # if the color is dark blue, we have to change S and V of the transfer color
    if darkblue:
        temp1 = (255 - originalColor[1])/2
        temp2 = (255 - originalColor[2])/2
    else:
        temp1 = 0
        temp2 = 0

    return np.array([temp, temp1, temp2])


def detectSuitableFrame(img):
    # used to detect a frame in the video, which contains green background and players (wide shot frame)
    # this frame is used for color detection
    hist = imgHistogram(img, None, 1, 0)
    sumi = 0
    for i in range(32, 61):
        sumi = sumi + hist[i][0]
    average = sumi/(61-32)
    if average > 20000 and average < 25000:
        return True
    return False    

