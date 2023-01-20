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
source_dir = 'P:/BaTh/Dataset4_22-04-22/dataAug_results_segmented'

crl_gt = os.path.join(source_dir, 'crl_gt_segmented')
crl_pred = os.path.join(source_dir, 'crl_pred_segmented')
crl = [crl_gt, crl_pred]

mir_gt = os.path.join(source_dir, 'mir_gt_segmented')
mir_pred = os.path.join(source_dir, 'mir_pred_segmented')
mir = [mir_gt, mir_pred]

noa_gt = os.path.join(source_dir, 'noa_gt_segmented')
noa_pred = os.path.join(source_dir, 'noa_pred_segmented')
noa = [noa_gt, noa_pred]

rot_gt = os.path.join(source_dir, 'rot_gt_segmented')
rot_pred = os.path.join(source_dir, 'rot_pred_segmented')
rot = [rot_gt, rot_pred]

dataAug_dirs = [crl, mir, rot, noa]

# setup for excel file and summary worksheet
dataAug_workb_path = 'C:/Users/Matthias Sagerer/Documents/TUM/bachelor_thesis/growth-prediction/results_xlsx/dataAug_metrics.xlsx'
dataAug_workb = xlwr.Workbook(dataAug_workb_path)
bold = dataAug_workb.add_format({'bold': True})
sum_worksh = dataAug_workb.add_worksheet('dataAug_summary')
sum_worksh.set_column(0, 0, 17)
sum_worksh.set_column(1, 8, 10)

metrics = ['IoU', 'Cell_Area', 'Precision', 'Recall']
for metric_nr, metric in enumerate(metrics):
    sum_worksh.write(f'{chr(65+2*metric_nr+1)}1', metric, bold)
    sum_worksh.write(f'{chr(65+2*metric_nr+1)}2', 'average', bold)
    sum_worksh.write(f'{chr(65+2*metric_nr+2)}2', 'st. dev.', bold)
    exec(f"worksh_{metric} = dataAug_workb.add_worksheet('{metric}')")
    exec(f"worksh_{metric}.set_column(0, 0, 14)")
    exec(f"worksh_{metric}.set_column(1, 4, 12)")
sum_worksh.write('A2', 'Dataset', bold)

datasets = ['Control', 'Mirrored', 'Rotated', 'No augmentation']
for dataset_nr, dataset_title in enumerate(datasets):
    sum_worksh.write(f'A{dataset_nr+3}', dataset_title)


for dataS_nr, dataS in enumerate(dataAug_dirs):
    # isolate current datasets and add column in metric worksheets
    cur_dataset = dataS[0].split('\\')[-1][:3]
    for m_nr, metric in enumerate(metrics):
        exec(
            f"worksh_{metric}.write(f'{chr(65+dataS_nr+1)}1', '{cur_dataset}', bold)")

    # path for gt and pred dir
    gt_path = dataS[0]
    pred_path = dataS[1]

    # create empty np.arrs for metric score of current dataset
    cur_dataS_ious = np.array([])
    cur_dataS_cell_areas = np.array([])
    cur_dataS_precisions = np.array([])
    cur_dataS_recalls = np.array([])

    # get video names
    vids_gt = os.listdir(gt_path)
    vids_pred = os.listdir(pred_path)

    for vid_nr, (vid_gt, vid_pred) in enumerate(zip(vids_gt, vids_pred)):
        # create list of gt/pred frames for current video
        vid_gt_path = os.path.join(gt_path, vid_gt)
        vid_pred_path = os.path.join(pred_path, vid_pred)
        frs_gt = os.listdir(vid_gt_path)
        frs_pred = os.listdir(vid_pred_path)

        # create empty lists for metric scores of current video
        cur_vid_ious = np.array([])
        cur_vid_cell_areas = np.array([])
        cur_vid_precisions = np.array([])
        cur_vid_recalls = np.array([])

        # write current video name in excel sheets
        if dataS_nr == 0:
            for metr_nr, metric in enumerate(metrics):
                exec(
                    f"worksh_{metric}.write(f'A{vid_nr+2}', '{vid_gt}', bold)")

        for frame, (fr_gt, fr_pred) in enumerate(zip(frs_gt[6:], frs_pred[6:])):
            # read gt/pred frames
            fr_gt_path = os.path.join(vid_gt_path, fr_gt)
            fr_pred_path = os.path.join(vid_pred_path, fr_pred)
            gt_fr = cv2.imread(fr_gt_path)
            pred_fr = cv2.imread(fr_pred_path)

            # calculate metric score
            iou_score = calIoU(gt_fr, pred_fr)
            cell_area = calCellArea(gt_fr, pred_fr)
            precision = calPrecision(gt_fr, pred_fr)
            recall = calRecall(gt_fr, pred_fr)

            # append metric scores to video and dataset lists
            cur_vid_ious = np.append(cur_vid_ious, [iou_score])
            cur_vid_cell_areas = np.append(cur_vid_cell_areas, [cell_area])
            cur_vid_precisions = np.append(cur_vid_precisions, [precision])
            cur_vid_recalls = np.append(cur_vid_recalls, [recall])

            cur_dataS_ious = np.append(cur_dataS_ious, [iou_score])
            cur_dataS_cell_areas = np.append(cur_dataS_cell_areas, [cell_area])
            cur_dataS_precisions = np.append(cur_dataS_precisions, [precision])
            cur_dataS_recalls = np.append(cur_dataS_recalls, [recall])

        # calculate video metric averages and write to excel sheets
        vid_iou_avg = cur_vid_ious.mean()
        vid_cell_area_avg = cur_vid_cell_areas.mean()
        vid_precision_avg = cur_vid_precisions.mean()
        vid_recall_avg = cur_vid_recalls.mean()

        metric_avgs = [vid_iou_avg, vid_cell_area_avg,
                       vid_precision_avg, vid_recall_avg]

        for metri_nr, metric in enumerate(metrics):
            cell = f'{chr(65+dataS_nr+1)}{vid_nr+2}'
            avg_val = metric_avgs[metri_nr]
            exec(
                f"worksh_{metric}.write_number('{cell}', {avg_val})")

        # print progress to cli
        tot_test_vid_num = len(dataAug_dirs)*len(vids_gt)
        cur_test_vid_num = dataS_nr*len(vids_gt)+vid_nr+1
        progress = round((cur_test_vid_num/tot_test_vid_num)*100, 1)
        print(f'dataAug metric progress: {progress} %')

    # calculate metric averages and st. dev. and write them to excel sheet
    dataS_iou_avg = cur_dataS_ious.mean()
    dataS_cell_area_avg = cur_dataS_cell_areas.mean()
    dataS_precision_avg = cur_dataS_precisions.mean()
    dataS_recall_avg = cur_dataS_recalls.mean()

    dataS_iou_std = cur_dataS_ious.std()
    dataS_cell_area_std = cur_dataS_cell_areas.std()
    dataS_precision_std = cur_dataS_precisions.std()
    dataS_recall_std = cur_dataS_recalls.std()

    dataS_avgs = [dataS_iou_avg, dataS_cell_area_avg,
                  dataS_precision_avg, dataS_recall_avg]

    dataS_stds = [dataS_iou_std, dataS_cell_area_std,
                  dataS_precision_std, dataS_recall_std]

    for me_nr, metric_name in enumerate(metrics):
        avg_cell = f'{chr(65+2*(me_nr+1)-1)}{dataS_nr+3}'
        std_cell = f'{chr(65+2*(me_nr+1))}{dataS_nr+3}'
        avg = dataS_avgs[me_nr]
        std = dataS_stds[me_nr]
        sum_worksh.write_number(avg_cell, avg)
        sum_worksh.write_number(std_cell, std)

        # for debugging
        # sum_worksh.write(avg_cell, f'avg{cur_dataset}{metrics[me_nr]}')
        # sum_worksh.write(std_cell, f'std{cur_dataset}{metrics[me_nr]}')

dataAug_workb.close()
