import numpy as np
import cv2


def apply_color_overlay(image,mask, intensity = 0.5,blue = 0, green = 0, red = 0):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image_h, image_w, image_c = image.shape

    # creating matrix of same img dimensions and filling it with required color divided by 255
    color_bgra = (blue / 255, green / 255, red / 255)
    overlay = np.full((image_h,image_w,3),color_bgra, dtype= 'float_')

    # converting the mask to desired color, and adding alpha channel initialized by ones
    tempMask = overlay*mask
    tempOnes = np.ones((image_h,image_w,1))
    temp=np.concatenate((tempMask,tempOnes), axis=2)

    # overlaying the mask on the image
    cv2.addWeighted(np.uint8(temp),intensity,image,1.0,0,image)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    return image


def removePitch(frame, lower_pitch_color, higher_pitch_color):
    count = 0
    idx = 0
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # extracting only the pitch
    mask = cv2.inRange(hsvFrame, lower_pitch_color, higher_pitch_color)
    maskedFrame = cv2.bitwise_and(hsvFrame, hsvFrame, mask=mask)

    # convert hsv to gray for thresholding
    maskedFrame_bgr = cv2.cvtColor(maskedFrame, cv2.COLOR_HSV2BGR)
    maskedFrame_gray = cv2.cvtColor(maskedFrame_bgr, cv2.COLOR_BGR2GRAY)

    # Performing closing to remove noise
    kernel = np.ones((10, 10), np.uint8)
    thresholdedMask = cv2.threshold(maskedFrame_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresholdedMask = cv2.morphologyEx(thresholdedMask, cv2.MORPH_CLOSE, kernel)

    return cv2.bitwise_and(frame, frame, mask=thresholdedMask)


def find_histogram(clt):
    # creating array with cluster numbers
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    # Finding Histogram
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # Normalizing Histogram from 0 to 1
    hist = hist.astype("float")
    hist /= hist.sum()

    return hist


def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


