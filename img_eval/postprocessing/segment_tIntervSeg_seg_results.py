import os
import sys
import cv2
import numpy as np


def genNumStr(num):
    num_str = str(num)
    add_zeros = '0'*(4-len(num_str))
    num_str = f'{add_zeros}{num_str}'
    return num_str


def segmentImg(img_input):
    img_copy = img_input.copy()
    lower_white = np.array([127, 127, 127], dtype='uint16')
    upper_white = np.array([255, 255, 255], dtype='uint16')
    thres_mask = cv2.inRange(img_copy, lower_white, upper_white)
    img_copy[thres_mask > 0] = (255, 255, 255)
    img_copy[thres_mask < 1] = (0, 0, 0)
    return img_copy


source_dir = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_sorted'

seg1h = os.path.join(source_dir, 'tests_seg1h_23-11-22_sorted')
seg2h = os.path.join(source_dir, 'tests_seg2h_23-11-22_sorted')
seg3h = os.path.join(source_dir, 'tests_seg3h_23-11-22_sorted')
seg4h = os.path.join(source_dir, 'tests_seg4h_08-12-22_sorted')

dirs_raw = [seg1h, seg2h, seg3h, seg4h]
dirs = []
for i, cur_dir in enumerate(dirs_raw):
    in_gt_dir = os.path.join(cur_dir, 'in_gt')
    in_pred_dir = os.path.join(cur_dir, 'in_pred')
    dirs.append(in_gt_dir)
    dirs.append(in_pred_dir)

segmented_path = os.path.join(source_dir, 'tIntervSeg_results_segment')
os.mkdir(segmented_path)

for h, cur_dir in enumerate(dirs):
    cur_dir_detail = cur_dir.split('/')[-1].split('\\')
    dir_type = ''
    if cur_dir_detail[2][-2:] == 'gt':
        dir_type = 'gt'
    else:
        dir_type = 'pred'
    cur_dir_info = f'{cur_dir_detail[1][6:11]}_{dir_type}'
    seg_dir_name = f'{cur_dir_info}_segmented'
    seg_dir = os.path.join(segmented_path, seg_dir_name)
    os.mkdir(seg_dir)
    cur_videos = os.listdir(cur_dir)
    for i, cur_vid in enumerate(cur_videos):
        cur_vid_seg = f'{cur_vid[:5]}_seg{cur_vid[-4:]}'
        cur_vid_seg_path = os.path.join(seg_dir, cur_vid_seg)
        os.mkdir(cur_vid_seg_path)
        cur_vid_path = os.path.join(cur_dir, cur_vid)
        cur_frames = os.listdir(cur_vid_path)
        cur_frames.pop()
        for j, cur_fr_name in enumerate(cur_frames):
            cur_fr_path = os.path.join(cur_vid_path, cur_fr_name)
            cur_fr = cv2.imread(cur_fr_path)
            cur_fr_seg = segmentImg(cur_fr)
            cur_fr_seg_name = f'{cur_fr_name[:-4]}seg{cur_fr_name[-4:]}'
            cur_fr_seg_path = os.path.join(cur_vid_seg_path, cur_fr_seg_name)
            cv2.imwrite(cur_fr_seg_path, cur_fr_seg)
        progress = round(
            ((h*len(cur_videos)+i+1)/(len(cur_videos)*len(dirs)))*100, 2)
        print(f'Segmenting results. Progress: {progress} %')
