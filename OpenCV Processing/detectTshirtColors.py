import cv2
import numpy as np

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans  # pip install scipy then pip install import sklearn.cluster
from AuxFunctions import find_histogram
from AuxFunctions import plot_colors2
from AuxFunctions import removePitch


def DominantColorsHistogram(img,noClusters):
    clusteringImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # flattening the matrix for training
    clusteringImg = clusteringImg.reshape((clusteringImg.shape[0] * clusteringImg.shape[1], 3))
    # Clustering
    clt = KMeans(n_clusters=noClusters)
    clt.fit(clusteringImg)
    print(clt)

    # Output Histogram
    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)

    plt.axis("off")
    plt.imshow(bar)
    plt.show()


def main():
    img = cv2.imread('IPTest.jpg')

    # Green color range for pitch detection
    lower_pitch_color = np.array([40, 40, 40])
    upper_pitch_color = np.array([70, 255, 255])

    # Extracting possible players pixels by removing background
    players = removePitch (img, lower_pitch_color, upper_pitch_color)
    cv2.imshow('players', players)
    cv2.waitKey()

    # Finding Contours in processed img
    playersGray = cv2.cvtColor(players, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(playersGray, 0, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Keeping only contours of height more than width (players) and discarding the rest
    newContours=[]
    for c in contours:
        # Rectangle around the contour, vertex at (x,y) width (w) height (h)
        x, y, w, h = cv2.boundingRect(c)
        if h >= 1.5 * w:
            if w > 15 and h >= 15:
                newContours.append(c)

    # Drawing contours around detected players
    cv2.drawContours(img, newContours, -1, (0, 255, 0), 3)

    cv2.imshow('players', img)
    cv2.waitKey()

    DominantColorsHistogram(img,6)


if __name__ =="__main__":
    main()