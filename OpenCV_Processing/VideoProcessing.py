import cv2
import numpy as np

import matplotlib.pyplot as plt

from OpenCV_Processing.ChangeTshirtColors import ChangeTshirtColors
from OpenCV_Processing.detectTshirtColors import extractShirtsColors
from OpenCV_Processing.AuxFunctions import calculateChangeColor, detectSuitableFrame


def VideoProcessing(Color1, Color2, start, end):

    video = cv2.VideoCapture('videos/video1.mp4')
    noFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    VideoTime=noFrames/fps
    print (noFrames)
    startFrame=noFrames*start/VideoTime
    print (startFrame)
    endFrame=noFrames*end/VideoTime
    print(endFrame)
    count=0
    while video.isOpened():
        ret, frame = video.read()
        if ret==True:
            if detectSuitableFrame(frame):
                    goodframe = frame
                    break
        #cv2.imshow('frame',frame)

    l1, u1, m1, l2, u2, m2 = extractShirtsColors(goodframe)
    frame_height, frame_width, _ = goodframe.shape
    outvideo = cv2.VideoWriter('videos/video2.mp4',cv2.VideoWriter_fourcc('M', 'P', 'E', 'G'), fps, (frame_width, frame_height))
    video1 = cv2.VideoCapture('videos/video1.mp4')

    # if the 2 detected ranges are the same, we will work on only one range
    if l1[0] == l2[0] and u1[0] == u2[0]:
        l2 = np.array([0, 0, 0])
        u2 = np.array([0, 0, 0])

    # choosing the 2 new colors for the teams
    color1 = calculateChangeColor(Color1, m1)
    color2 = calculateChangeColor(Color2, m2)
    count=0
    while video1.isOpened():
        count = count+1
        ret, frame = video1.read()
        if ret  and count >startFrame :
            recoloredFrame = ChangeTshirtColors(frame, l1, u1, color1, l2, u2, color2)
            outvideo.write(recoloredFrame)
        if  count >endFrame   :
            break
        # cv2.imshow('frame',frame)
    video.release()
    cv2.destroyAllWindows()
def main():
    VideoProcessing([150,40,40], [80,40,40],10, 30)
if __name__ == "__main__":
    main()