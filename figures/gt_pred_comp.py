import numpy as np
import os
import sys
import cv2

project_path = os.getcwd()
print(project_path)
sys.path.append(project_path)
from tools.disp_mult_img import imreadRelPath, dispImgs


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

    gt_rel_paths = [os.path.join(gt_path, fname)
                    for i, fname in enumerate(gt_files)]
    gt_frs = [imreadRelPath(path) for i, path in enumerate(gt_rel_paths)]
    gt_frs = np.hstack(tuple(gt_frs))

    gt_start_paths = [os.path.join(gt_path, fname)
                      for i, fname in enumerate(gt_start)]
    gt_start_frs = [imreadRelPath(path)
                    for i, path in enumerate(gt_start_paths)]
    gt_start_frs = np.hstack(tuple(gt_start_frs))

    pred_files = os.listdir(pred_path)

    # select last 6 frames
    pred_files[:] = pred_files[6:12]
    # create one image from prediction frames
    pred_rel_paths = [os.path.join(pred_path, fname)
                      for i, fname in enumerate(pred_files)]
    pred_frs = [imreadRelPath(path) for i, path in enumerate(pred_rel_paths)]
    pred_frs = np.hstack(tuple(pred_frs))
    pred_frs = segmentImg(pred_frs)

    # show coloured difference between ground truth and prediction
    frs_and = cv2.bitwise_and(gt_frs, pred_frs)  # intersection
    frs_or = cv2.bitwise_or(gt_frs, pred_frs)   # union
    frs_xor = cv2.bitwise_xor(gt_frs, pred_frs)  # union - intersection

    frs_pred_less = cv2.bitwise_and(frs_xor, gt_frs)
    frs_pred_less = segmentImg(frs_pred_less)
    frs_pred_less[np.where((frs_pred_less == [255, 255, 255]).all(axis=2))] = [
        255, 0, 0]

    frs_pred_more = cv2.bitwise_and(frs_xor, pred_frs)
    frs_pred_more = segmentImg(frs_pred_more)
    frs_pred_more[np.where((frs_pred_more == [255, 255, 255]).all(axis=2))] = [
        0, 255, 0]

    frs_diff = cv2.bitwise_or(frs_pred_less, frs_pred_more)
    frs_diff = cv2.bitwise_or(frs_diff, frs_and)

    # unite all images to one image and add border between first/last 6 frames
    bor_pxs = (10, 5)
    border = np.full((bor_pxs[0], 128*6, 3), (127, 127, 127), dtype=np.uint8)
    border_small = np.full(
        (bor_pxs[1], 128*6, 3), (127, 127, 127), dtype=np.uint8)
    comps = [gt_start_frs, border, gt_frs,
             border_small, pred_frs, border_small, frs_diff]
    frs_comp = np.vstack(tuple(comps))

    # write labels on image
    labels = ['First six frames', 'Ground truth', 'Prediction',
              'Prediction of more(green)/less(blue) growth']
    y_offset = [0, bor_pxs[0], bor_pxs[0]+bor_pxs[1],
                bor_pxs[0]+2*bor_pxs[1], bor_pxs[0]+3*bor_pxs[1]]
    for i in range(len(comps)-3):
        cv2.putText(frs_comp, labels[i], (0, i*128+20+y_offset[i]),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 69, 255), 1)

    return frs_comp


ext_results_dir = 'P:/BaTh/Dataset4_22-04-22/dataSframeR_results_sorted'
res_256px_18vids = os.path.join(ext_results_dir, 'trained_256px_18vids')
res_256px_45vids = os.path.join(ext_results_dir, 'trained_256px_45vids')
res_256px_90vids = os.path.join(ext_results_dir, 'trained_256px_90vids')
res_256px_180vids = os.path.join(ext_results_dir, 'trained_256px_180vids')
comp_1 = createPredGtComp(genVideoPaths(res_256px_18vids, 1))
comp_2 = createPredGtComp(genVideoPaths(res_256px_45vids, 1))
comp_3 = createPredGtComp(genVideoPaths(res_256px_90vids, 1))
comp_4 = createPredGtComp(genVideoPaths(res_256px_180vids, 1))
cv2.imwrite(
    'C:/Users/Matthias Sagerer/Downloads/comp_256px_18vids_v001.png', comp_1)
cv2.imwrite(
    'C:/Users/Matthias Sagerer/Downloads/comp_256px_45vids_v001.png', comp_2)
cv2.imwrite(
    'C:/Users/Matthias Sagerer/Downloads/comp_256px_90vids_v001.png', comp_3)
cv2.imwrite(
    'C:/Users/Matthias Sagerer/Downloads/comp_256px_180vids_v001.png', comp_4)

dispImgs([comp_1, comp_2, comp_3, comp_4])
