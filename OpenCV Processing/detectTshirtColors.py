import cv2
import numpy as np

import matplotlib.pyplot as plt
from AuxFunctions import removeBackGround
from AuxFunctions import imgHistogram
from AuxFunctions import maxRangeFromHisto


# we will detect the max color (background) then remove it
# then detect the max color again (one of the teams now), get its range and then remove it also
# then detect max color for third time (second team), now we have the 2 teams color ranges and will return them
def extractShirtsColors (img):
    # finding histogram for H channel of full frame (channel 0)
    hist = imgHistogram(img, None, 1, 0)
    histS = imgHistogram(img, None, 1, 1)
    histV = imgHistogram(img, None, 1, 2)
    maxIndex = np.argmax(hist)
    maxIndexS = np.argmax(histS)
    maxIndexV = np.argmax(histV)
    # getting the max color range
    startIndex, endIndex = maxRangeFromHisto(maxIndex,maxIndexS,maxIndexV)

    # Green color range for pitch detection
    lower_pitch_color = np.array([startIndex[0], startIndex[1], startIndex[2]])
    upper_pitch_color = np.array([endIndex[0], endIndex[1], endIndex[2]])

    # Extracting possible players pixels by removing background
    players = removeBackGround(img, lower_pitch_color, upper_pitch_color)

    # Finding Contours in processed img
    playersGray = cv2.cvtColor(players, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(playersGray, 0, 255, 0)
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Keeping only contours of height more than width (players) and discarding the rest
    newContours = []
    playersPixels = np.zeros_like(img)
    for c in contours:
        # Rectangle around the contour, vertex at (x,y) width (w) height (h)
        x, y, w, h = cv2.boundingRect(c)
        if h >= 1.5 * w:
            if w > 15 and h >= 15:
                newContours.append(c)

    # filling the new contours with white, then anding with original image
    for i in range(len(newContours)):
        cv2.drawContours(playersPixels, newContours, i, color=(255, 255, 255), thickness=-1)
    playersPixels = playersPixels & img
    hist = imgHistogram(img, playersPixels, 0, 0)
    histS = imgHistogram(img, playersPixels, 0, 1)
    histV = imgHistogram(img, playersPixels, 0, 2)

    # plt.plot(hist, color='r')
    # plt.xlim([0, 256])
    # plt.show()

    maxIndex = np.argmax(hist)
    maxIndexS = np.argmax(histS)
    maxIndexV = np.argmax(histV)
    # getting the max color range
    startIndex, endIndex = maxRangeFromHisto(maxIndex,maxIndexS,maxIndexV)

    lower_shirt_color = np.array([startIndex[0], startIndex[1], startIndex[2]])
    upper_shirt_color = np.array([endIndex[0], endIndex[1], endIndex[2]])

    # removing background and players of 1st team, leaving only players of 2nd team
    playersSameTeam = removeBackGround(playersPixels, lower_shirt_color, upper_shirt_color)
    playersSameTeam = removeBackGround(playersSameTeam, lower_pitch_color, upper_pitch_color)

    # second team only players histogram
    hist = imgHistogram(img, playersSameTeam, 0, 0)
    histS = imgHistogram(img, playersSameTeam, 0, 1)
    histV = imgHistogram(img, playersSameTeam, 0, 2)
    plt.plot(hist, color='r')
    plt.xlim([0, 256])
    plt.show()


    maxIndex = np.argmax(hist)
    maxIndexS = np.argmax(histS)
    maxIndexV = np.argmax(histV)
    # getting the max color range
    startIndex, endIndex = maxRangeFromHisto(maxIndex,maxIndexS,maxIndexV)
    print(startIndex, endIndex)

    lower_shirt2_color = np.array([startIndex[0], startIndex[1], startIndex[2]])
    upper_shirt2_color = np.array([endIndex[0], endIndex[1], endIndex[2]])

    return lower_shirt_color, upper_shirt_color, lower_shirt2_color, upper_shirt2_color


def main():
    img = cv2.imread('IPTest2.jpg')
    l1, u1, l2, u2 = extractShirtsColors(img)
    print(l1, u1, l2, u2)


if __name__ == "__main__":
    main()