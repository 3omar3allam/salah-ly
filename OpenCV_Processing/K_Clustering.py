import cv2
import numpy as np

import matplotlib.pyplot as plt






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


def DominantColorsHistogram(img,noClusters):
    clusteringImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    clusteringImg2 = cv2.cvtColor(clusteringImg, cv2.COLOR_BGR2HSV)

    clusteringImg = clusteringImg.reshape((clusteringImg.shape[0] * clusteringImg.shape[1], 3))

    clt = KMeans(n_clusters=noClusters)
    clt.fit(clusteringImg)
    print(clt)

    # Output Histogram
    hist = find_histogram(clt)s
    bar = plot_colors2(hist, clt.cluster_centers_)

    plt.axis("off")
    plt.imshow(bar)
    plt.show()


def main():
    img = cv2.imread('IPTest.jpg')
    DominantColorsHistogram(img, 6)


if __name__ == "__main__":
    main()

