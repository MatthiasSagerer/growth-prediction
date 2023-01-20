import cv2
import numpy as np

size = 1.5


def resize(img, factor=size):
    new_shape = (int(img.shape[1]*factor), int(img.shape[0]*factor))
    img_res = cv2.resize(img, new_shape)
    return img_res


edg_gt = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_edg1h_24-11-22_sorted/in_gt/video0001/video0001_frame0007_R128x128.png')
seg_gt = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_seg1h_23-11-22_sorted/in_gt/video0001/video0001_frame0007_R128x128.png')

edg_pred = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_edg1h_24-11-22_sorted/in_pred/video0001/video0001_frame0007_R128x128.png')
seg_pred = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_seg1h_23-11-22_sorted/in_pred/video0001/video0001_frame0007_R128x128.png')

seg_gt = resize(seg_gt)
edg_gt = resize(edg_gt)

seg_pred = resize(seg_pred)
edg_pred = resize(edg_pred)

b_col = (127, 127, 127)
b_small_size = 4
b_big_size = 8

b_small = np.full((int(128*size), b_small_size, 3), b_col, dtype=np.uint8)
b_big = np.full((int(128*size), b_big_size, 3), b_col, dtype=np.uint8)

fig = np.hstack((edg_gt, b_small, edg_pred, b_big, seg_gt, b_small, seg_pred))

cv2.imshow('figure', fig)
cv2.waitKey(0)

# cv2.imwrite('C:/Users/Matthias Sagerer/Downloads/tIntervSeg_edg_seg_comp.png', fig)
