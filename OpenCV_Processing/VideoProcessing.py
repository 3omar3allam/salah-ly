import cv2
import numpy as np

import matplotlib.pyplot as plt

from OpenCV_Processing.ChangeTshirtColors import ChangeTshirtColors
from OpenCV_Processing.detectTshirtColors import extractShirtsColors
from OpenCV_Processing.AuxFunctions import calculateChangeColor, detectSuitableFrame


def VideoProcessing(Color1, Color2, start, end):

    video = cv2.VideoCapture('videos/temp/video1.mp4')
    while video.isOpened():
        ret, frame = video.read()
        if ret==True:
            if detectSuitableFrame(frame):
                    goodframe = frame
                    break
        #cv2.imshow('frame',frame)

    l1, u1, m1, l2, u2, m2 = extractShirtsColors(goodframe)
    frame_height, frame_width, _ = goodframe.shape
    outvideo = cv2.VideoWriter('..//videos//temp//video2.avi',cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame_width, frame_height))

    # if the 2 detected ranges are the same, we will work on only one range
    if l1[0] == l2[0] and u1[0] == u2[0]:
        l2 = np.array([0, 0, 0])
        u2 = np.array([0, 0, 0])

    # choosing the 2 new colors for the teams
    color1 = calculateChangeColor(Color1, m1)
    color2 = calculateChangeColor(Color2, m2)     
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            recoloredFrame = ChangeTshirtColors(frame, l1, u1, color1, l2, u2, color2)
            outvideo.write(recoloredFrame)
        else:
            break     
        # cv2.imshow('frame',frame)
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()  