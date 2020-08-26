import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


def show_wait_destroy(winname, img):
    plt_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgplot = plt.imshow(plt_image)
    plt.show()


def remove_underline(path, show = False):
    src = cv.imread(path, cv.IMREAD_COLOR)
    if src is None:
        print ("L'image s'ouvre pas "  + path)
        return -1
    cv.imshow("src", src)
    if len(src.shape) != 2:
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    else:
        gray = src
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                                cv.THRESH_BINARY, 15, -2)
    horizontal = np.copy(bw)
    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv.erode(horizontal, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 10 # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 2  # minimum number of pixels making up a line
    max_line_gap = 10000  # maximum gap in pixels between connectable line segments
    line_image = np.copy(src) * 0  # creating a blank to draw lines on
    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(horizontal, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    y_max = src.shape[0]
    for line in lines:
        for x1,y1,x2,y2 in line:
            if(y1>100 and y2>100 and y1<1300 and y2<1300 and x2-x1>200):
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
                src[y1:y_max,x1:x2,:] = (255, 255, 255)
                cv2.rectangle(line_image, (x1, y_max), (x2,y_max), (0, 0, 255), 2)
    lines_edges = cv2.addWeighted(src, 0.8, line_image, 1, 0)
    if(show):
        plt_image = cv2.cvtColor(lines_edges, cv2.COLOR_BGR2RGB)
        imgplot = plt.imshow(plt_image)
        plt.show()
    return src


if __name__ == "__main__":
    im = remove_underline("exemple4.JPEG", show=False)
    plt_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    imgplot = plt.imshow(plt_image)
    plt.show()
