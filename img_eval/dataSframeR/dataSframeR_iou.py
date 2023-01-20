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
source_dir = 'P:/BaTh/Dataset4_22-04-22/dataSframeR_results_segmented'
# 18vids
res128px_18vids_gt = os.path.join(source_dir, 'res128px18vids_gt_segmented')
res256px_18vids_gt = os.path.join(source_dir, 'res256px18vids_gt_segmented')
res512px_18vids_gt = os.path.join(source_dir, 'res512px18vids_gt_segmented')
res660px_18vids_gt = os.path.join(source_dir, 'res660px18vids_gt_segmented')

res128px_18vids_pred = os.path.join(
    source_dir, 'res128px18vids_pred_segmented')
res256px_18vids_pred = os.path.join(
    source_dir, 'res256px18vids_pred_segmented')
res512px_18vids_pred = os.path.join(
    source_dir, 'res512px18vids_pred_segmented')
res660px_18vids_pred = os.path.join(
    source_dir, 'res660px18vids_pred_segmented')

res128px_18vids_dirs = [res128px_18vids_gt, res128px_18vids_pred]
res256px_18vids_dirs = [res256px_18vids_gt, res256px_18vids_pred]
res512px_18vids_dirs = [res512px_18vids_gt, res512px_18vids_pred]
res660px_18vids_dirs = [res660px_18vids_gt, res660px_18vids_pred]

size_18vids_dirs = [res128px_18vids_dirs, res256px_18vids_dirs,
                    res512px_18vids_dirs, res660px_18vids_dirs]

# 45vids
res128px_45vids_gt = os.path.join(source_dir, 'res128px45vids_gt_segmented')
res256px_45vids_gt = os.path.join(source_dir, 'res256px45vids_gt_segmented')
res512px_45vids_gt = os.path.join(source_dir, 'res512px45vids_gt_segmented')
res660px_45vids_gt = os.path.join(source_dir, 'res660px45vids_gt_segmented')

res128px_45vids_pred = os.path.join(
    source_dir, 'res128px45vids_pred_segmented')
res256px_45vids_pred = os.path.join(
    source_dir, 'res256px45vids_pred_segmented')
res512px_45vids_pred = os.path.join(
    source_dir, 'res512px45vids_pred_segmented')
res660px_45vids_pred = os.path.join(
    source_dir, 'res660px45vids_pred_segmented')

res128px_45vids_dirs = [res128px_45vids_gt, res128px_45vids_pred]
res256px_45vids_dirs = [res256px_45vids_gt, res256px_45vids_pred]
res512px_45vids_dirs = [res512px_45vids_gt, res512px_45vids_pred]
res660px_45vids_dirs = [res660px_45vids_gt, res660px_45vids_pred]

size_45vids_dirs = [res128px_45vids_dirs, res256px_45vids_dirs,
                    res512px_45vids_dirs, res660px_45vids_dirs]

# 90vids
res128px_90vids_gt = os.path.join(source_dir, 'res128px90vids_gt_segmented')
res256px_90vids_gt = os.path.join(source_dir, 'res256px90vids_gt_segmented')
res512px_90vids_gt = os.path.join(source_dir, 'res512px90vids_gt_segmented')
res660px_90vids_gt = os.path.join(source_dir, 'res660px90vids_gt_segmented')

res128px_90vids_pred = os.path.join(
    source_dir, 'res128px90vids_pred_segmented')
res256px_90vids_pred = os.path.join(
    source_dir, 'res256px90vids_pred_segmented')
res512px_90vids_pred = os.path.join(
    source_dir, 'res512px90vids_pred_segmented')
res660px_90vids_pred = os.path.join(
    source_dir, 'res660px90vids_pred_segmented')

res128px_90vids_dirs = [res128px_90vids_gt, res128px_90vids_pred]
res256px_90vids_dirs = [res256px_90vids_gt, res256px_90vids_pred]
res512px_90vids_dirs = [res512px_90vids_gt, res512px_90vids_pred]
res660px_90vids_dirs = [res660px_90vids_gt, res660px_90vids_pred]

size_90vids_dirs = [res128px_90vids_dirs, res256px_90vids_dirs,
                    res512px_90vids_dirs, res660px_90vids_dirs]

# 180vids
res128px_180vids_gt = os.path.join(source_dir, 'res128px180vids_gt_segmented')
res256px_180vids_gt = os.path.join(source_dir, 'res256px180vids_gt_segmented')
res512px_180vids_gt = os.path.join(source_dir, 'res512px180vids_gt_segmented')
res660px_180vids_gt = os.path.join(source_dir, 'res660px180vids_gt_segmented')

res128px_180vids_pred = os.path.join(
    source_dir, 'res128px180vids_pred_segmented')
res256px_180vids_pred = os.path.join(
    source_dir, 'res256px180vids_pred_segmented')
res512px_180vids_pred = os.path.join(
    source_dir, 'res512px180vids_pred_segmented')
res660px_180vids_pred = os.path.join(
    source_dir, 'res660px180vids_pred_segmented')

res128px_180vids_dirs = [res128px_180vids_gt, res128px_180vids_pred]
res256px_180vids_dirs = [res256px_180vids_gt, res256px_180vids_pred]
res512px_180vids_dirs = [res512px_180vids_gt, res512px_180vids_pred]
res660px_180vids_dirs = [res660px_180vids_gt, res660px_180vids_pred]

size_180vids_dirs = [res128px_180vids_dirs, res256px_180vids_dirs,
                     res512px_180vids_dirs, res660px_180vids_dirs]

# This list contains a list (video number) of lists (frame resolution) of lists (gt, pred)
dataSframeR_dirs = [size_18vids_dirs, size_45vids_dirs,
                    size_90vids_dirs, size_180vids_dirs]

# setup for excel file and summary worksheet
dataSframeR_workb_path = 'C:/Users/Matthias Sagerer/Documents/TUM/bachelor_thesis/growth-prediction/results_xlsx/dataSframeR/dataSframeR_iou.xlsx'
dataSframeR_workb = xlwr.Workbook(dataSframeR_workb_path)
bold = dataSframeR_workb.add_format({'bold': True})
sum_worksh = dataSframeR_workb.add_worksheet('dataSframeR_summary')
sum_worksh.set_column(0, 0, 17)
sum_worksh.set_column(1, 8, 10)

dataset_sizes = ['18vids', '45vids', '90vids', '180vids']
for i, dataS in enumerate(dataset_sizes):
    sum_worksh.write(f'{chr(65+2*i+1)}1', dataS, bold)
    sum_worksh.write(f'{chr(65+2*i+1)}2', 'average', bold)
    sum_worksh.write(f'{chr(65+2*i+2)}2', 'st. dev.', bold)
sum_worksh.write('A2', 'Resolution', bold)

resolutions = ['128px', '256px', '512px', '660px']
for i, resolution_title in enumerate(resolutions):
    sum_worksh.write(f'A{i+3}', resolution_title, bold)

for dataS_nr, cur_dataS_dirs in enumerate(dataSframeR_dirs):
    # isolate current dataset size and setup 18/45/90/180 worksheets
    cur_dataS = cur_dataS_dirs[0][0].split('/')[-1].split('\\')[-1][8:-13]
    exec(f"worksh_{cur_dataS} = dataSframeR_workb.add_worksheet('{cur_dataS}')")
    exec(f"worksh_{cur_dataS}.set_column(0, 0, 14)")
    exec(f"worksh_{cur_dataS}.set_column(1, 4, 12)")
    for i, res_title in enumerate(resolutions):
        exec(f"worksh_{cur_dataS}.write('{chr(65+i+1)}1', '{res_title}', bold)")

    for res_nr, cur_res_dirs in enumerate(cur_dataS_dirs):
        # isolate current resolution
        cur_res = cur_res_dirs[0].split('\\')[-1][3:8]

        # path for gt and pred dir
        gt_path = cur_res_dirs[0]
        pred_path = cur_res_dirs[1]

        # create empty np.arr for metric scores of current dataSframeR
        cur_dataSframeR_metric_scores = np.array([])

        # get video names
        vids_gt = os.listdir(gt_path)
        vids_pred = os.listdir(pred_path)

        for vid_nr, (vid_gt, vid_pred) in enumerate(zip(vids_gt, vids_pred)):
            # create list of gt/pred frames for current video
            vid_gt_path = os.path.join(gt_path, vid_gt)
            vid_pred_path = os.path.join(pred_path, vid_pred)
            frs_gt = os.listdir(vid_gt_path)
            frs_pred = os.listdir(vid_pred_path)

            # create empty list for metric scores of current video
            vid_metric_scores = np.array([1])

            # write current video name in excel sheet
            exec(f"worksh_{cur_dataS}.write('A{vid_nr+2}', '{vid_gt}', bold)")

            for frame, (fr_gt, fr_pred) in enumerate(zip(frs_gt[6:], frs_pred[6:])):
                # read gt/pred frame and calculate metric score
                fr_gt_path = os.path.join(vid_gt_path, fr_gt)
                fr_pred_path = os.path.join(vid_pred_path, fr_pred)
                gt_fr = cv2.imread(fr_gt_path)
                pred_fr = cv2.imread(fr_pred_path)
                metric_score = calIoU(gt_fr, pred_fr)

                # append metric score to video list
                vid_metric_scores = np.append(
                    vid_metric_scores, [metric_score])
                cur_dataSframeR_metric_scores = np.append(
                    cur_dataSframeR_metric_scores, [metric_score])

            # calculate video metric average and write to excel sheet
            vid_metric_avg = vid_metric_scores.mean()
            exec(
                f"worksh_{cur_dataS}.write_number('{chr(65+res_nr+1)}{vid_nr+2}', {vid_metric_avg})")

            # print progress to cli
            tot_test_vid_num = len(dataSframeR_dirs) * \
                len(cur_dataS_dirs)*len(vids_gt)
            cur_test_vid_num = (dataS_nr*len(cur_dataS_dirs) +
                                res_nr)*len(vids_gt)+vid_nr+1
            progress = round((cur_test_vid_num/tot_test_vid_num)*100, 2)
            print(f'dataSframeR metric progress: {progress} %')

        # calculate metric avg and st. dev. and write them to excel sheet
        cur_dataSframeR_metric_avg = cur_dataSframeR_metric_scores.mean()
        cur_dataSframeR_metric_std = cur_dataSframeR_metric_scores.std()
        sum_worksh.write_number(
            f'{chr(65+2*(dataS_nr+1)-1)}{res_nr+3}', cur_dataSframeR_metric_avg)
        sum_worksh.write_number(
            f'{chr(65+2*(dataS_nr+1))}{res_nr+3}', cur_dataSframeR_metric_std)

dataSframeR_workb.close()
