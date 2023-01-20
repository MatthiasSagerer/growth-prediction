import cv2
import numpy as np
import matplotlib.pyplot as plt


def callback(x):
    print(x)


img_path = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_edg1h_24-11-22_sorted/in_pred/video0001/video0001_frame0001_R128x128.png'

img = cv2.imread(img_path, 0)  # read image as grayscale
img_copy = img.copy()
img_resized = cv2.resize(img_copy, (512, 512))
fin_img = cv2.Canny(img, 85, 255)
fin_img = cv2.resize(fin_img, (512, 512))

cv2.namedWindow('image')  # make a window with name 'image'
# lower threshold trackbar for window 'image
cv2.createTrackbar('L', 'image', 0, 64, callback)
# upper threshold trackbar for window 'image
cv2.createTrackbar('U', 'image', 0, 64, callback)
# gauss 1 trackbar for window 'image
cv2.createTrackbar('G1', 'image', 0, 25, callback)
# dilate trackbar for window 'image
cv2.createTrackbar('dilate', 'image', 0, 25, callback)
# dilate iterations trackbar for window 'image
cv2.createTrackbar('d_iter', 'image', 0, 25, callback)
# erode trackbar for window 'image
cv2.createTrackbar('erode', 'image', 0, 25, callback)
# erode iterations trackbar for window 'image
cv2.createTrackbar('e_iter', 'image', 0, 25, callback)
# gauss 2 trackbar for window 'image
cv2.createTrackbar('G2', 'image', 0, 25, callback)
# threshold min trackbar for window 'image
cv2.createTrackbar('Min', 'image', 0, 255, callback)
# threshold max trackbar for window 'image
cv2.createTrackbar('Max', 'image', 0, 255, callback)

while(1):
    numpy_horizontal_concat = np.concatenate(
        (img_resized, fin_img), axis=1)  # to display image side by side
    cv2.imshow('image', numpy_horizontal_concat)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # escape key
        break

    l = cv2.getTrackbarPos('L', 'image')
    u = cv2.getTrackbarPos('U', 'image')
    g1 = cv2.getTrackbarPos('G1', 'image') * 2 + 1
    d = cv2.getTrackbarPos('dilate', 'image') * 2 + 1
    d_iter = cv2.getTrackbarPos('d_iter', 'image')
    e = cv2.getTrackbarPos('erode', 'image') * 2 + 1
    e_iter = cv2.getTrackbarPos('e_iter', 'image')
    g2 = cv2.getTrackbarPos('G2', 'image') * 2 + 1
    min = cv2.getTrackbarPos('Min', 'image')
    max = cv2.getTrackbarPos('Max', 'image')

    # for 128x128
    # l, u, g1, g2, min, max = 10, 40, 1*2+1, 3*2+1, 10, 255

    # for 512x512
    l, u = 12, 20
    g1, g2 = 0*2+1, 16*2+1
    d, e = 2, 0
    d_iter, e_iter = 2, 0
    min, max = 0, 255

    kernel_dil = np.ones((d, d), np.uint8)
    kernel_ero = np.ones((e, e), np.uint8)

    img = cv2.resize(img, (512, 512))
    erode = cv2.erode(img, kernel_ero, iterations=e_iter)
    gauss1 = cv2.GaussianBlur(erode, (g1, g1), 0)
    canny = cv2.Canny(gauss1, l, u)
    dilate = cv2.dilate(canny, kernel_dil, iterations=d_iter)
    gauss2 = cv2.GaussianBlur(dilate, (g2, g2), 0)
    ret, fin_img = cv2.threshold(
        gauss2, min, max, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    fin_img = cv2.resize(fin_img, (128, 128))
    fin_img = cv2.resize(fin_img, (512, 512))

cv2.destroyAllWindows()
