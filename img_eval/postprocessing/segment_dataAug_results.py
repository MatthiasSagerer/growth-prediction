import os
import sys
import cv2
import numpy as np
from PIL import Image

counter = 0


def calcOccurringPxVals(img):
    img_conv = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_conv).convert('L')
    pixel_values = set(list(pil_img.getdata()))
    return pixel_values


def genNumStr(num, digits=4):
    num_str = str(num)
    add_zeros = '0'*(digits-len(num_str))
    num_str = f'{add_zeros}{num_str}'
    return num_str


def simpleSegmentImg(img_input):
    img_copy = img_input.copy()
    lower_white = np.array([127, 127, 127], dtype='uint16')
    upper_white = np.array([255, 255, 255], dtype='uint16')
    thres_mask = cv2.inRange(img_copy, lower_white, upper_white)
    img_copy[thres_mask > 0] = (255, 255, 255)
    img_copy[thres_mask < 1] = (0, 0, 0)

    # check if only px values 0 and 255 are existed in the segmented image
    px_vals = calcOccurringPxVals(img_copy)
    if px_vals != {0, 255}:
        print(px_vals)

    return img_copy


def segmentImg(img_input):
    # create copies
    img_copy = img_input.copy()

    # set good parameter values values for thresholding process
    dil = 2
    # ero = 1
    can_l, can_u = 12, 20
    # gauss1 = 1*2+1
    gauss2 = 18*2+1
    thres_min, thres_max = 0, 255

    # set kernels for dilate and erode
    kernel_dil = np.ones((dil, dil), np.uint8)
    # kernel_ero = np.ones((ero, ero), np.uint8)

    # resize and apply dilate, erode, gaussian blur, canny edge detection and thresholding
    img_res = cv2.resize(img_copy, (512, 512))
    # img_erode = cv2.erode(img_res, kernel_ero, iterations=1)
    # img_gauss1 = cv2.GaussianBlur(img_erode, (gauss1, gauss1), 0)
    img_canny = cv2.Canny(img_res, can_l, can_u)
    img_dilate = cv2.dilate(img_canny, kernel_dil, iterations=3)
    img_gauss2 = cv2.GaussianBlur(img_dilate, (gauss2, gauss2), 0)
    ret, img_thres = cv2.threshold(
        img_gauss2, thres_min, thres_max, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_seg = cv2.resize(img_thres, (128, 128))

    # set all pixel values to 0, 255
    cut_off = 192
    img_seg[img_seg > cut_off] = 255
    img_seg[img_seg < cut_off] = 0

    # check if only px values 0 and 255 are existed in the segmented image
    # print(calcOccurringPxVals(img_seg))

    return img_seg


# define source and target directory
source_dir = 'P:/BaTh/Dataset4_22-04-22/dataAug_results_sorted'
target_dir = 'P:/BaTh/Dataset4_22-04-22/dataAug_results_segmented'

# name relevant subdirectories of source directors
control = os.path.join(source_dir, 'tests_crl_13-12-22_sorted')
mirror = os.path.join(source_dir, 'tests_mir_21-12-22_sorted')
no_aug = os.path.join(source_dir, 'tests_noa_21-12-22_sorted')
rotated = os.path.join(source_dir, 'tests_rot_21-12-22_sorted')

# merge all relevant directories as a list of tuples
dirs_raw = [control, mirror, no_aug, rotated]
dirs = []
for i, cur_dir in enumerate(dirs_raw):
    in_gt_dir = os.path.join(cur_dir, 'in_gt')
    in_pred_dir = os.path.join(cur_dir, 'in_pred')
    dirs.append(in_gt_dir)
    dirs.append(in_pred_dir)

counter = 0

for h, cur_dir in enumerate(dirs):
    # create (path for) directory with segmented videos from current directory
    cur_dir_detail = cur_dir.split('/')[-1].split('\\')
    dir_type = ''
    if cur_dir_detail[-1][-2:] == 'gt':
        dir_type = 'gt'
    else:
        dir_type = 'pred'
    cur_dir_info = f"{cur_dir_detail[1][6:9]}_{dir_type}"
    seg_dir_name = f'{cur_dir_info}_segmented'
    seg_dir = os.path.join(target_dir, seg_dir_name)
    os.mkdir(seg_dir)

    # create list with the videos of the current directory
    cur_videos = os.listdir(cur_dir)
    for i, cur_vid in enumerate(cur_videos):

        # create (path for) directory with segmented frames from current video
        cur_vid_seg = f'{cur_vid[:5]}_seg{cur_vid[-4:]}'
        cur_vid_seg_path = os.path.join(seg_dir, cur_vid_seg)
        os.mkdir(cur_vid_seg_path)

        # create list with frames of current video and remove .gif-file
        cur_vid_path = os.path.join(cur_dir, cur_vid)
        cur_frames = os.listdir(cur_vid_path)
        cur_frames.pop()
        for j, cur_fr_name in enumerate(cur_frames):

            # segment current frame
            cur_fr_path = os.path.join(cur_vid_path, cur_fr_name)

            cur_fr = cv2.imread(cur_fr_path)
            cur_fr_seg = simpleSegmentImg(cur_fr)

            # create path for segmented frame and save it
            cur_fr_seg_name = f'{cur_fr_name[:-4]}seg{cur_fr_name[-4:]}'
            cur_fr_seg_path = os.path.join(cur_vid_seg_path, cur_fr_seg_name)
            cv2.imwrite(cur_fr_seg_path, cur_fr_seg)
            counter += 1

        # print progress of segmentation process to the console (accurate to a video)
        progress = round(
            ((h*len(cur_videos)+i+1)/(len(cur_videos)*len(dirs)))*100, 2)
        print(f'Segmenting results. Progress: {progress} %')

print(f'Finished segmentation of {counter} frames. :D')
