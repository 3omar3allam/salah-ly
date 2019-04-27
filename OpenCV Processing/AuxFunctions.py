import numpy as np
import cv2


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
    maskedFrame = cv2.bitwise_and(hsvFrame, hsvFrame, mask=mask)

    # convert hsv to gray for thresholding
    maskedFrame_bgr = cv2.cvtColor(maskedFrame, cv2.COLOR_HSV2BGR)
    maskedFrame_gray = cv2.cvtColor(maskedFrame_bgr, cv2.COLOR_BGR2GRAY)

    # Performing closing to remove noise
    kernel = np.ones((10, 10), np.uint8)
    thresholdedMask = cv2.threshold(maskedFrame_gray, 0, 255, cv2.THRESH_BINARY)[1]
    thresholdedMask = cv2.morphologyEx(thresholdedMask, cv2.MORPH_CLOSE, kernel)

    # subtracting to get only the players without the background
    removedBackground = frame-cv2.bitwise_and(frame, frame, mask=thresholdedMask)

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
    hist = cv2.calcHist([imageHSV], [channelNo], thresholdedMask, [256], [0, 256])
    return hist


def maxRangeFromHisto (H,maxIndexH,X):
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
    startIndex=0
    endIndex=0
    if maxIndexH<=8:
        startIndex=0
        endIndex=8
    elif maxIndexH<=37 :
        startIndex=9
        endIndex=37
    elif maxIndexH<=75 :
        startIndex=38
        endIndex=75        
    elif maxIndexH<=146 :
        startIndex=76
        endIndex=146        
    elif maxIndexH<=207 :
        startIndex=147
        endIndex=207        
    elif maxIndexH<=277 :
        startIndex=208
        endIndex=277    
    elif maxIndexH<=346 :
        startIndex=278
        endIndex=346        
    elif maxIndexH<=360 :
        startIndex=347
        endIndex=360  
    # if maxIndexS<=25:
    #     startIndex[1]=0
    #     endIndex[1]=25
    # elif maxIndexS<=34 :
    #     startIndex[1]=26
    #     endIndex[1]=34
    # elif maxIndexS<=59 :
    #     startIndex[1]=35
    #     endIndex[1]=59
    # elif maxIndexS<=79 :
    #     startIndex[1]=60
    #     endIndex[1]=79
    # elif maxIndexS<=87 :
    #     startIndex[1]=80
    #     endIndex[1]=87
    # elif maxIndexS<=100 :
    #     startIndex[1]=88
    #     endIndex[1]=100
    # if maxIndexV<=3:
    #     startIndex[2]=0
    #     endIndex[2]=3
    # elif maxIndexV<=8 :
    #     startIndex[2]=4
    #     endIndex[2]=8
    # elif maxIndexV<=39 :
    #     startIndex[2]=9
    #     endIndex[2]=39
    # elif maxIndexV<=75 :
    #     startIndex[2]=40
    #     endIndex[2]=75
    # elif maxIndexV<=100 :
    #     startIndex[2]=76
    #     endIndex[2]=100
    startIndex=int(round(startIndex/360*180))
    # endIndex=int(round(endIndex/360*180 ))
    # startIndex[1]=int(round(startIndex[1]/100*255))
    # endIndex[1]=int(round(endIndex[1]/100*255))
    # startIndex[2]=int(round(startIndex[2]/100*255))
    # endIndex[2]=int(round(endIndex[2]/100*255))
    return startIndex,endIndex                                                                                                              
    # HSVColors=[]
    # HSVColors.append([[0,360],[0,100],[0,3]]) #[[Hrange][Srange][Vrange]] Black 
    # HSVColors.append([[0,360],[0,25],[96,100]]) #[[Hrange][Srange][Vrange]] around white

    # HSVColors.append([[0,8],[26,34],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[35,59],[76,100]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[60,79],[76,100]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[80,87],[76,100]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[88,100],[76,100]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[26,34],[8,39]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[35,59],[8,39]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[60,79],[8,39]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[80,87],[8,39]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[0,8],[88,100],[8,39]]) #[[Hrange][Srange][Vrange]]



    # HSVColors.append([[9,37],[26,34],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[80,87],[40,75]])  #[[Hrange][Srange][Vrange]]
    # HSVColors.append([[9,37],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]




    # HSVColors.append([[38,75],[26,34],[40,75]])  #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[80,87],[40,75]])#[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[38,75],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   

    # HSVColors.append([[76,146],[26,34],[40,75]])  #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[80,87],[40,75]])#[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[76,146],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   

    # HSVColors.append([[147,207],[26,34],[40,75]])  #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[147,207],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   

    # HSVColors.append([[208,277],[26,34],[40,75]])  #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[26,34],[76,100]])#[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[208,277],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   

    # HSVColors.append([[278,346],[26,34],[40,75]])  #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[278,346],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   

    # HSVColors.append([[347,360],[26,34],[40,75]])  #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[35,59],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[60,79],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[80,87],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[26,34],[76,100]]) #[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[35,59],[40,75]] )#[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[60,79],[40,75]] )#[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[80,87],[40,75]] )#[[Hrange][Srange][Vrange]]   
    # HSVColors.append([[347,360],[88,100],[40,75]]) #[[Hrange][Srange][Vrange]]   
    

