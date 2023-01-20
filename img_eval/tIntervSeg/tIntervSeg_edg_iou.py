import os
import cv2
import xlsxwriter as xlwr
import numpy as np


def upscaleAndShowImg(img1, img2, img1_txt='image 1', img2_txt='image 2', size=512, delay=0):
    img1_upscaled = cv2.resize(img1, (size, size))
    img2_upscaled = cv2.resize(img2, (size, size))
    cv2.imshow(img1_txt, img1_upscaled)
    cv2.imshow(img2_txt, img2_upscaled)
    cv2.waitKey(delay)


def calIoU(img1, img2):
    img1_arr = np.asarray(img1)
    img2_arr = np.asarray(img2)
    intersection = np.logical_and(img1_arr, img2_arr)
    union = np.logical_or(img1_arr, img2_arr)
    iou_img1_img2 = np.sum(intersection)/np.sum(union)
    return iou_img1_img2


def calCellArea(gt_img, pred_img):
    gt_img_arr = np.asarray(gt_img)
    pred_img_arr = np.asarray(pred_img)
    gt_cell_area = np.sum(gt_img_arr)
    pred_cell_area = np.sum(pred_img_arr)
    pred_cell_area_norm = pred_cell_area/gt_cell_area
    return pred_cell_area_norm


def calPrecision(gt_img, pred_img):
    gt_img_arr = np.asarray(gt_img)
    pred_img_arr = np.asarray(pred_img)
    pred_img_arr_bol = np.logical_and(pred_img_arr, pred_img_arr)
    intersection = np.logical_and(gt_img_arr, pred_img_arr)
    precision = np.sum(intersection)/np.sum(pred_img_arr_bol)
    return precision


def calRecall(gt_img, pred_img):
    gt_img_arr = np.asarray(gt_img)
    gt_img_arr_bol = np.logical_and(gt_img_arr, gt_img_arr)
    pred_img_arr = np.asarray(pred_img)
    intersection = np.logical_and(gt_img_arr, pred_img_arr)
    recall = np.sum(intersection)/np.sum(gt_img_arr_bol)
    return recall


# setup of paths
source_dir = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg_results_segmented'

edg1h_gt = os.path.join(source_dir, 'edg1h_gt_segmented')
edg2h_gt = os.path.join(source_dir, 'edg2h_gt_segmented')
edg3h_gt = os.path.join(source_dir, 'edg3h_gt_segmented')
edg4h_gt = os.path.join(source_dir, 'edg4h_gt_segmented')

edg1h_pred = os.path.join(source_dir, 'edg1h_pred_segmented')
edg2h_pred = os.path.join(source_dir, 'edg2h_pred_segmented')
edg3h_pred = os.path.join(source_dir, 'edg3h_pred_segmented')
edg4h_pred = os.path.join(source_dir, 'edg4h_pred_segmented')

edg1h_dirs = [edg1h_gt, edg1h_pred]
edg2h_dirs = [edg2h_gt, edg2h_pred]
edg3h_dirs = [edg3h_gt, edg3h_pred]
edg4h_dirs = [edg4h_gt, edg4h_pred]

edg_dirs = [edg1h_dirs, edg2h_dirs, edg3h_dirs, edg4h_dirs]

# setup for excel file and summary worksheet
edg_workb_path = 'C:/Users/Matthias Sagerer/Documents/TUM/bachelor_thesis/growth-prediction/results_xlsx/tIntervSeg_edg/tIntervSeg_edg_iou.xlsx'
edg_workb = xlwr.Workbook(edg_workb_path)
bold = edg_workb.add_format({'bold': True})
sum_worksh = edg_workb.add_worksheet('edg_summary')
sum_worksh.set_column(0, 0, 17)
sum_worksh.set_column(1, 8, 10)
for hour in range(1, 5):
    exec(f"sum_worksh.write('{chr(65+2*hour-1)}1', 'edg{hour}h', bold)")
    exec(f"sum_worksh.write('{chr(65+2*hour-1)}2', 'average', bold)")
    exec(f"sum_worksh.write('{chr(65+2*hour)}2', 'st. dev.', bold)")
sum_worksh.write('A2', 'Frame', bold)
sum_worksh.write('A9', 'average', bold)

# create empty lists for metric means/standard deviation
metric_means = []
metric_stds = []

for fr in range(1, 7):
    exec(f"sum_worksh.write_number('A{fr+2}', {fr})")

for dir_nr, dirs in enumerate(edg_dirs):
    # get path for gt and pred
    gt_path = dirs[0]
    pred_path = dirs[1]

    # isolate dir_type for worksheet names
    dir_type = gt_path.split()[-1].split('\\')[-1][:5]
    print(dir_type)

    # setup for edg1/2/3/4h worksheets
    exec(f"{dir_type}_worksh = edg_workb.add_worksheet('{dir_type}')")
    exec(f"{dir_type}_worksh.set_column(0, 0, 14)")
    exec(f"{dir_type}_worksh.set_column(1, 6, 12)")
    for frame_nr in range(1, 7):
        exec(f"{dir_type}_worksh.write('{chr(65+frame_nr)}1', 'Frame {frame_nr}', bold)")

    # create empty lists for metric scores
    for frame in range(1, 7):
        exec(f"fr{frame}_metric_scores = []")

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

            # read gt/pred img and calculate metric
            fr_gt_path = os.path.join(vid_gt_path, fr_gt)
            fr_pred_path = os.path.join(vid_pred_path, fr_pred)
            cur_gt_fr = cv2.imread(fr_gt_path)
            cur_pred_fr = cv2.imread(fr_pred_path)
            metric = calIoU(cur_gt_fr, cur_pred_fr)

            # append metric to list and write to excel sheet
            exec(f"fr{frame-6}_metric_scores.append({metric})")
            exec(f"{dir_type}_worksh.write_number('{chr(66+frame-7)}{j+2}', {metric})")

        # print progress to cli
        progress = round((dir_nr*83+j+1)/(len(edg_dirs)*83)*100, 2)
        print(f'Edg metric progress: {progress} %')

    dir_metric_means = []
    dir_metric_stds = []

    # calculate metric mean and standard deviation for frames and write them to excel sheet
    for fr_nr in range(1, 7):
        exec(f"fr{fr_nr}_metric_scores_arr = np.array(fr{fr_nr}_metric_scores)")
        exec(f"metric_mean = fr{fr_nr}_metric_scores_arr.mean()")
        exec(f"metric_std = fr{fr_nr}_metric_scores_arr.std()")
        dir_metric_means.append(metric_mean)
        dir_metric_stds.append(metric_std)
        metric_means.append(metric_mean)
        metric_stds.append(metric_std)
        metric_mean = round(metric_mean, 6)
        metric_std = round(metric_std, 6)
        exec(
            f"sum_worksh.write_number('{chr(65+2*(dir_nr+1)-1)}{fr_nr+2}', {metric_mean})")
        exec(
            f"sum_worksh.write_number('{chr(65+2*(dir_nr+1))}{fr_nr+2}', {metric_std})")

    # calculate directory metric and standard deviation means and write to excel file
    dir_metric_means_arr = np.array(dir_metric_means)
    dir_metric_stds_arr = np.array(dir_metric_stds)
    dir_mean = dir_metric_means_arr.mean()
    dir_mean_std = dir_metric_stds_arr.mean()
    dir_mean = round(dir_mean, 6)
    dir_mean_std = round(dir_mean_std, 6)
    exec(f"sum_worksh.write_number('{chr(65+2*(dir_nr+1)-1)}{9}', {dir_mean})")
    exec(
        f"sum_worksh.write_number('{chr(65+2*(dir_nr+1))}{9}', {dir_mean_std})")

# calculate total metric mean and total mean metric deviation and write to excel file
metric_means_arr = np.array(metric_means)
metric_stds_arr = np.array(metric_stds)
total_mean = metric_means_arr.mean()
total_mean_std = metric_stds_arr.mean()
total_mean = round(total_mean, 6)
total_mean_std = round(total_mean_std, 6)
sum_worksh.write('A11', 'Total avg IoU')
sum_worksh.write('A12', 'Total avg std')
sum_worksh.write_number('B11', total_mean)
sum_worksh.write_number('B12', total_mean_std)

edg_workb.close()
