import cv2
import numpy as np

import matplotlib.pyplot as plt

from ChangeTshirtColors import ChangeTshirtColors
from detectTshirtColors import extractShirtsColors
from AuxFunctions import calculateChangeColor
from AuxFunctions import detectSuitableFrame

def VideoProcessing(Color1,Color2) :
    video = cv2.VideoCapture('..//videos//temp//video1.mp4')
    while(video.isOpened()):
        ret, frame = video.read()
        if(ret==True):
            if detectSuitableFrame(frame):
                    goodframe=frame
                    break
        #cv2.imshow('frame',frame)
    l1, u1, m1, l2, u2, m2 = extractShirtsColors(goodframe)
    frame_height, frame_width, _ = goodframe.shape
    outvideo = cv2.VideoWriter('..//videos//temp//video2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))    
    # if the 2 detected ranges are the same, we will work on only one channel
    if l1[0] == l2[0] and u1[0] == u2[0]:
        l2 = np.array([0, 0, 0])
        u2 = np.array([0, 0, 0])
    # choosing the 2 new colors for the teams, choose one of the colors and put its number in the 1st argument of the fn
    # (0:red) (1:orange) (2:yellow) (3:green) (4:dark green) (5:light blue) (6:blue)
    # (7:dark blue) (8:light violet) (9:dark violet) (-1:no change)
    color1 = calculateChangeColor(Color1, m1)
    color2 = calculateChangeColor(Color2, m2)     
    while(video.isOpened()):
        ret, frame = video.read()
        if(ret==True):
            recoloredFrame = ChangeTshirtColors(frame, l1, u1, color1, l2, u2, color2)
            outvideo.write(recoloredFrame)
        else :
            break     
        #cv2.imshow('frame',frame)
    video.release()
    cv2.destroyAllWindows()
def main():
    #VideoProcessing(0,7)
if __name__ == "__main__":
    main()  