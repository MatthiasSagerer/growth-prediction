import cv2
import numpy as np

size = 1.5


def resize(img, factor=size):
    new_shape = (int(img.shape[1]*factor), int(img.shape[0]*factor))
    img_res = cv2.resize(img, new_shape)
    return img_res


gt1h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori1h_22-12-22_sorted/in_gt/video0001/video0001_frame0007_R128x128.png')
gt2h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori2h_02-12-22_sorted/in_gt/video0003/video0003_frame0007_R128x128.png')
gt3h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori3h_01-12-22_sorted/in_gt/video0005/video0005_frame0007_R128x128.png')
gt4h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori4h_08-12-22_sorted/in_gt/video0005/video0005_frame0007_R128x128.png')

pred1h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori1h_22-12-22_sorted/in_pred/video0001/video0001_frame0007_R128x128.png')
pred2h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori2h_02-12-22_sorted/in_pred/video0003/video0003_frame0007_R128x128.png')
pred3h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori3h_01-12-22_sorted/in_pred/video0005/video0005_frame0007_R128x128.png')
pred4h = cv2.imread(
    'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted/tests_ori4h_08-12-22_sorted/in_pred/video0005/video0005_frame0007_R128x128.png')

gt1h = resize(gt1h)
gt2h = resize(gt2h)
gt3h = resize(gt3h)
gt4h = resize(gt4h)

pred1h = resize(pred1h)
pred2h = resize(pred2h)
pred3h = resize(pred3h)
pred4h = resize(pred4h)

b_color = (0, 0, 0)
img_size = int(128*size)
w_h_bor = 8
w_v_bor = 4
h_bor = np.full((img_size, w_h_bor, 3), b_color, dtype=np.uint8)
v_bor = np.full((w_v_bor, 4*img_size+3*w_h_bor, 3), b_color, dtype=np.uint8)

gt = np.hstack((gt1h, h_bor, gt2h, h_bor, gt3h, h_bor, gt4h))
pred = np.hstack((pred1h, h_bor, pred2h, h_bor, pred3h, h_bor, pred4h))

fig = np.vstack((gt, v_bor, pred))

print(fig.shape)
cv2.imshow('figure', fig)
cv2.waitKey(0)

# cv2.imwrite('C:/Users/Matthias Sagerer/Downloads/tIntervSeg_ori_comp.png', fig)
