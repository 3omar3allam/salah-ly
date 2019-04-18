import numpy as np
import cv2
import cv2 as cv

def apply_color_overlay(image,mask, intensity = 0.5,blue = 0, green = 0, red = 0):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_h, image_w, image_c = image.shape
    color_bgra = (blue / 255, green / 255, red / 255)
    overlay = np.full((image_h,image_w,3),color_bgra, dtype= 'float_')
    tempMask=overlay*mask
    cv2.imshow('Video', tempMask)
    tempOnes=np.ones((image_h,image_w,1))

    temp=np.concatenate((tempMask,tempOnes), axis=2)
    cv2.addWeighted(np.uint8(temp),intensity,image,1.0,0,image)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    cv2.waitKey()
    return image


# im_width = 320
# im_height = 240
# cap = cv2.VideoCapture("F:\Salah-ly\France v Belgium - 2018 FIFA World Cup Russia™ - Match 61.mp4")
# cap.set(cv.CAP_PROP_FRAME_WIDTH,im_width)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT,im_height)
img = cv2.imread('IPTest.jpg')
frame=img
# cv.namedWindow("Video", 0)
# The order of the colors is blue, green, red
lower_color_bounds = (40, 0, 0)
upper_color_bounds = (225,90,90)
# print ('Press <q> to quit')
# while(cap.isOpened()):
#  ret,frame = cap.read()
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
mask = cv2.inRange(frame,lower_color_bounds,upper_color_bounds )
mask_rgb = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
frame = frame & mask_rgb
ret,thresh1 = cv2.threshold(frame,0,255,cv2.THRESH_BINARY)
frame2=apply_color_overlay(img,thresh1,1,0,255,255)
cv2.imshow('Video',frame2)
cv2.imshow('Video2',thresh1)
cv2.waitKey()
 # if (cv2.waitKey(1) & 0xFF == ord('q')):
 #  cv.DestroyWindow("video")
 #  break
# cap.release()
# cv2.destroyAllWindows()