import numpy as np
import cv2


def apply_color_overlay(image,mask, intensity = 0.5,blue = 0, green = 0, red = 0):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_h, image_w, image_c = image.shape
    color_bgra = (blue / 255, green / 255, red / 255)
    overlay = np.full((image_h,image_w,3),color_bgra, dtype= 'float_')
    tempMask=overlay*mask
    tempOnes=np.ones((image_h,image_w,1))

    temp=np.concatenate((tempMask,tempOnes), axis=2)
    cv2.addWeighted(np.uint8(temp),intensity,image,1.0,0,image)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return image
