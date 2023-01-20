import cv2
import numpy as np


def addFrame(img, width=4, color=(127, 127, 127)):
    img_copy = img.copy()
    v_border = np.full((width, img_copy.shape[1], 3), color, dtype=np.uint8)
    h_border = np.full(
        (img_copy.shape[0]+2*width, width, 3), color, dtype=np.uint8)

    img_copy = np.vstack((v_border, img_copy, v_border))
    img_copy = np.hstack((h_border, img_copy, h_border))

    return img_copy


img = cv2.imread('C:/path/to/read/img')

img = addFrame(img)

cv2.imshow('Image', img)
cv2.waitKey(0)

cv2.imwrite('C:/path/to/write/image')
