import os
import cv2
import xlsxwriter as xlwr
import numpy as np


def calIoU(img1, img2):
    img1_arr = np.asarray(img1)
    img2_arr = np.asarray(img2)
    intersection = np.logical_and(img1_arr, img2_arr)
    union = np.logical_or(img1_arr, img2_arr)
    iou_img1_img2 = np.sum(intersection)/np.sum(union)
    return iou_img1_img2


# setup of paths
source_dir = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_segment'

seg1h_gt = os.path.join(source_dir, 'seg1h_gt_segmented')
seg2h_gt = os.path.join(source_dir, 'seg2h_gt_segmented')
seg3h_gt = os.path.join(source_dir, 'seg3h_gt_segmented')
seg4h_gt = os.path.join(source_dir, 'seg4h_gt_segmented')

seg1h_pred = os.path.join(source_dir, 'seg1h_pred_segmented')
seg2h_pred = os.path.join(source_dir, 'seg2h_pred_segmented')
seg3h_pred = os.path.join(source_dir, 'seg3h_pred_segmented')
seg4h_pred = os.path.join(source_dir, 'seg4h_pred_segmented')

seg1h_dirs = [seg1h_gt, seg1h_pred]
seg2h_dirs = [seg2h_gt, seg2h_pred]
seg3h_dirs = [seg3h_gt, seg3h_pred]
seg4h_dirs = [seg4h_gt, seg4h_pred]

seg_dirs = [seg1h_dirs, seg2h_dirs, seg3h_dirs, seg4h_dirs]

# setup for excel file and summary worksheet
seg_workb_path = 'C:/Users/Matthias Sagerer/Documents/TUM/bachelor_thesis/growth-prediction/results_xlsx/tIntervSeg_seg_iou.xlsx'
seg_workb = xlwr.Workbook(seg_workb_path)
bold = seg_workb.add_format({'bold': True})
sum_worksh = seg_workb.add_worksheet('seg_summary')
sum_worksh.set_column(0, 0, 15)
sum_worksh.set_column(1, 8, 10)
for hour in range(1, 5):
    exec(f"sum_worksh.write('{chr(65+2*hour-1)}1', 'seg{hour}h', bold)")
    exec(f"sum_worksh.write('{chr(65+2*hour-1)}2', 'average', bold)")
    exec(f"sum_worksh.write('{chr(65+2*hour)}2', 'st. dev.', bold)")
sum_worksh.write('A2', 'Frame', bold)
sum_worksh.write('A9', 'average', bold)

# create empty lists for IoU means/standard deviation
iou_means = []
iou_stds = []

for fr in range(1, 7):
    exec(f"sum_worksh.write_number('A{fr+2}', {fr})")

for dir_nr, dirs in enumerate(seg_dirs):
    # get path for gt and pred
    gt_path = dirs[0]
    pred_path = dirs[1]

    # isolate dir_type for worksheet names
    dir_type = gt_path.split()[-1].split('\\')[-1][:5]
    print(dir_type)

    # setup for seg1/2/3/4h worksheets
    exec(f"{dir_type}_worksh = seg_workb.add_worksheet('{dir_type}')")
    exec(f"{dir_type}_worksh.set_column(0, 0, 14)")
    exec(f"{dir_type}_worksh.set_column(1, 6, 12)")
    for frame_nr in range(1, 7):
        exec(f"{dir_type}_worksh.write('{chr(65+frame_nr)}1', 'Frame {frame_nr}', bold)")

    # create empty list for IoUs
    for frame in range(1, 7):
        exec(f"fr{frame}_ious = []")

    # get video names
    vids_gt = os.listdir(gt_path)
    vids_pred = os.listdir(pred_path)

    for j, (vid_gt, vid_pred) in enumerate(zip(vids_gt, vids_pred)):
        # create lists of gt/pred frames
        vid_gt_path = os.path.join(gt_path, vid_gt)
        vid_pred_path = os.path.join(pred_path, vid_pred)
        frs_gt = os.listdir(vid_gt_path)
        frs_pred = os.listdir(vid_pred_path)

        # write video names in excel sheet
        exec(f"{dir_type}_worksh.write('A{j+2}', '{vid_gt}', bold)")
        for frame, (fr_gt, fr_pred) in enumerate(zip(frs_gt[6:], frs_pred[6:]), 7):

            # read gt/pred img and calculate IoU
            fr_gt_path = os.path.join(vid_gt_path, fr_gt)
            fr_pred_path = os.path.join(vid_pred_path, fr_pred)
            cur_gt_fr = cv2.imread(fr_gt_path)
            cur_pred_fr = cv2.imread(fr_pred_path)
            iou_score = calIoU(cur_gt_fr, cur_pred_fr)

            # append IoU to list and write to excel sheet
            exec(f"fr{frame-6}_ious.append({iou_score})")
            exec(
                f"{dir_type}_worksh.write_number('{chr(66+frame-7)}{j+2}', {iou_score})")

        # print progress to cli
        progress = round((dir_nr*83+j+1)/(len(seg_dirs)*83)*100, 2)
        print(f'Seg IoU progress: {progress} %')

    dir_iou_means = []
    dir_iou_stds = []

    # calculate IoU mean and standard deviation for frames and write them to excel sheet
    for fr_nr in range(1, 7):
        exec(f"fr{fr_nr}_ious_arr = np.array(fr{fr_nr}_ious)")
        exec(f"iou_mean = fr{fr_nr}_ious_arr.mean()")
        exec(f"iou_std = fr{fr_nr}_ious_arr.std()")
        dir_iou_means.append(iou_mean)
        dir_iou_stds.append(iou_std)
        iou_means.append(iou_mean)
        iou_stds.append(iou_std)
        iou_mean = round(iou_mean, 6)
        iou_std = round(iou_std, 6)
        exec(
            f"sum_worksh.write_number('{chr(65+2*(dir_nr+1)-1)}{fr_nr+2}', {iou_mean})")
        exec(
            f"sum_worksh.write_number('{chr(65+2*(dir_nr+1))}{fr_nr+2}', {iou_std})")

    # calculate directory IoU and standard deviation means and write to excel file
    dir_iou_means_arr = np.array(dir_iou_means)
    dir_iou_stds_arr = np.array(dir_iou_stds)
    dir_mean = dir_iou_means_arr.mean()
    dir_mean_std = dir_iou_stds_arr.mean()
    dir_mean = round(dir_mean, 6)
    dir_mean_std = round(dir_mean_std, 6)
    exec(f"sum_worksh.write_number('{chr(65+2*(dir_nr+1)-1)}{9}', {dir_mean})")
    exec(
        f"sum_worksh.write_number('{chr(65+2*(dir_nr+1))}{9}', {dir_mean_std})")

# calculate total IoU mean and total mean IoU deviation and write to excel file
iou_means_arr = np.array(iou_means)
iou_stds_arr = np.array(iou_stds)
total_mean = iou_means_arr.mean()
total_mean_std = iou_stds_arr.mean()
total_mean = round(total_mean, 6)
total_mean_std = round(total_mean_std, 6)
sum_worksh.write('A11', 'Total avg IoU')
sum_worksh.write('A12', 'Total avg std')
sum_worksh.write_number('B11', total_mean)
sum_worksh.write_number('B12', total_mean_std)

seg_workb.close()
