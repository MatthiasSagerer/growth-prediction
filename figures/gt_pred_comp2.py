import cv2
import os
import sys
import numpy as np

project_path = os.getcwd()
print(project_path)
sys.path.append(project_path)
from tools.disp_mult_img import imreadRelPath

w_border = 4
b_color = (127, 127, 127)
FN_col = (255, 0, 255)  # magenta false negative
FP_col = (0, 255, 0)  # green false positive


def segmentImg(img):
    lower_white = np.array([127, 127, 127], dtype='uint16')
    upper_white = np.array([255, 255, 255], dtype='uint16')
    thres_mask = cv2.inRange(img, lower_white, upper_white)
    img[thres_mask > 0] = (255, 255, 255)
    img[thres_mask < 1] = (0, 0, 0)
    return img


def genNumStr(num):
    num_str = str(num)
    add_zeros = '0'*(4-len(num_str))
    num_str = f'{add_zeros}{num_str}'
    return num_str


def genVideoPaths(vid_dir, vid_num):
    gt_path = os.path.join(vid_dir, f'in_gt/video{genNumStr(vid_num)}')
    pred_path = os.path.join(vid_dir, f'in_pred/video{genNumStr(vid_num)}')
    return (gt_path, pred_path)


def createPredGtComp(paths):
    gt_path = paths[0]
    pred_path = paths[1]
    gt_files = os.listdir(gt_path)

    # split between first and last 6 frames
    gt_start = gt_files[0:6]
    gt_files[:] = gt_files[6:12]

    hborder = np.full((128, w_border, 3), b_color, dtype=np.uint8)

    gt_rel_paths = [os.path.join(gt_path, fname)
                    for i, fname in enumerate(gt_files)]

    gt_frs = []
    for i, path in enumerate(gt_rel_paths):
        gt_frs.append(imreadRelPath(path))
        if i < 5:
            gt_frs.append(hborder)

    gt_frs = np.hstack(tuple(gt_frs))

    pred_files = os.listdir(pred_path)

    # select last 6 frames
    pred_files[:] = pred_files[6:12]
    # create one image from prediction frames
    pred_rel_paths = [os.path.join(pred_path, fname)
                      for i, fname in enumerate(pred_files)]

    pred_frs = []
    for i, path in enumerate(pred_rel_paths):
        pred_frs.append(imreadRelPath(path))
        if i < 5:
            pred_frs.append(hborder)

    pred_frs = np.hstack(tuple(pred_frs))
    pred_frs = segmentImg(pred_frs)

    # show coloured difference between ground truth and prediction
    frs_and = cv2.bitwise_and(gt_frs, pred_frs)  # intersection
    frs_or = cv2.bitwise_or(gt_frs, pred_frs)   # union
    frs_xor = cv2.bitwise_xor(gt_frs, pred_frs)  # union - intersection

    frs_pred_less = cv2.bitwise_and(frs_xor, gt_frs)
    frs_pred_less = segmentImg(frs_pred_less)
    frs_pred_less[np.where(
        (frs_pred_less == [255, 255, 255]).all(axis=2))] = list(FN_col)

    frs_pred_more = cv2.bitwise_and(frs_xor, pred_frs)
    frs_pred_more = segmentImg(frs_pred_more)
    frs_pred_more[np.where(
        (frs_pred_more == [255, 255, 255]).all(axis=2))] = list(FP_col)

    frs_diff = cv2.bitwise_or(frs_pred_less, frs_pred_more)
    frs_diff = cv2.bitwise_or(frs_diff, frs_and)

    for i in range(5):
        frs_diff[:, 128*(i+1) + w_border*i: 128*(i+1) +
                 w_border*(i+1)] = b_color

    return frs_diff


# set directory
dataAug_results_dir = 'P:/BaTh/Dataset4_22-04-22/dataAug_results_sorted'
crl = os.path.join(dataAug_results_dir, 'tests_crl_13-12-22_sorted')
size = 2

img_bath = createPredGtComp(genVideoPaths(crl, 3))

# cv2.imwrite(
#     'C:/Users/Matthias Sagerer/Downloads/dataAug_crl_video0003.png', img_bath)
# cv2.imshow('img', img_bath)
# cv2.waitKey(0)


# view ground truth prediction differences for all 83 tested videos
# for i in range(83):
#     img = createPredGtComp(genVideoPaths(crl, i+1))
#     img = cv2.resize(img, (int(img.shape[1]*size), int(img.shape[0]*size)))
#     # cv2.imshow(f'video{genNumStr(i)}', img)
#     cv2.waitKey(0)
#     cv2.destroyWindow(f'video{genNumStr(i)}')
