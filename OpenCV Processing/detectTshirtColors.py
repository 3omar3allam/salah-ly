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
    # hist = imgHistogram(img, None, 1, 0)
    # maxIndex = np.argmax(hist)
    # getting the max color range
    hist = imgHistogram(img, None, 1, 0)
    maxHist=np.argmax(hist)

    # plt.plot(hist, color='r')
    # plt.xlim([0, 180])
    # plt.show()
    startIndex, endIndex = maxRangeFromHisto(maxHist)  # getting the range of the playground color

    # Green color range for pitch detection
    lower_pitch_color = np.array([startIndex, 0, 0])
    upper_pitch_color = np.array([endIndex, 255, 255])

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
            if w > 10 and h >= 10:
                newContours.append(c)

    # filling the new contours with white, then anding with original image
    for i in range(len(newContours)):
        cv2.drawContours(playersPixels, newContours, i, color=(255, 255, 255), thickness=-1)
    playersPixels = playersPixels & img
    hist = imgHistogram(img, playersPixels, 0, 0)

    # plt.plot(hist, color='r')
    # plt.xlim([0, 256])
    # plt.show()

    maxIndex = np.argmax(hist)
    # getting the max color range
    startIndex, endIndex = maxRangeFromHisto(maxIndex)

    lower_shirt_color = np.array([startIndex, 40, 5])
    upper_shirt_color = np.array([endIndex, 255, 255])
    Red = False
    if lower_shirt_color[0] > upper_shirt_color[0]:
        Red = True

    # removing background and players of 1st team, leaving only players of 2nd team
    if Red:
        playersSameTeam = removeBackGround(playersPixels, lower_shirt_color, np.array([180, 255, 255]))
        playersSameTeam = removeBackGround(playersSameTeam, np.array([0, 40, 2]), upper_shirt_color)
    else:
        playersSameTeam = removeBackGround(playersPixels, lower_shirt_color, upper_shirt_color)

    playersSameTeam = removeBackGround(playersSameTeam, lower_pitch_color, upper_pitch_color)

    # second team only players histogram
    hist = imgHistogram(img, playersSameTeam, 0, 0)
    # plt.plot(hist, color='r')
    # plt.xlim([0, 256])
    # plt.show()

    maxIndex = np.argmax(hist)
    # getting the max color range
    startIndex, endIndex = maxRangeFromHisto(maxIndex)

    lower_shirt2_color = np.array([startIndex, 40, 5])
    upper_shirt2_color = np.array([endIndex, 255, 255])

    return lower_shirt_color, upper_shirt_color, lower_shirt2_color, upper_shirt2_color


def main():
    img = cv2.imread('Test_Cases//IPTest2.jpg')
    l1, u1, l2, u2 = extractShirtsColors(img)
    print(l1, u1, l2, u2)


if __name__ == "__main__":
    main()