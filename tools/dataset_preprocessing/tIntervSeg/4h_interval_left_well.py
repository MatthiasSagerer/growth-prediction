# Target of preprocessing:
# 728 videos (resolution: 512x512) with 12 frames each := 12FrVi

import tifffile as tiff
from matplotlib import pyplot as plt
import os
from PIL import Image


def genNumStr(num, digits=3):
    num_str = str(num)
    add_zeros = '0'*(digits-len(num_str))
    num_str = f'{add_zeros}{num_str}'
    return num_str


def setVideoNums(current_subdir, test_num, train_num, increase=False):
    if current_subdir == 'test':
        video_num = test_num
        if increase:
            test_num += 1
    elif current_subdir == 'train':
        video_num = train_num
        if increase:
            train_num += 1
    else:
        print("Error in 'increaseVideoNum': wrong input subdir")
    return video_num, test_num, train_num


# read in tif file and initialize most variables
source_dir = 'P:/BaTh/Dataset4_22-04-22/04_edited_files_matze'

# original
# left_well = tiff.imread(os.path.join(source_dir, '03_left_well_72frames.tif'))

# segmented
# left_well = tiff.imread(os.path.join(source_dir, '07_left_well_auto_threshold.tif'))

# find edges
# left_well = tiff.imread(os.path.join(source_dir, '04_left_well_find_edges_72fr.tif'))

x_offset = 0
y_offset = 0
fr_series = 1
cols = 14
rows = 13
video_num = 0
test_video_num = 0
train_video_num = 0
counter = 0

# select directory to save the processed frames
target_dir = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg'

# original
# dir = os.path.join(target_dir, 'ori_4h')

# segmented
# dir = os.path.join(target_dir, 'seg_4h')

# find edges
# dir = os.path.join(target_dir, 'edg_4h')

# create test/train folder and overview file
os.mkdir(os.path.join(dir, 'train'))
os.mkdir(os.path.join(dir, 'test'))
overview_file_path = os.path.join(dir, '4h_overview_left_well.txt')
with open(overview_file_path, 'w') as file:
    file.write('File overview for 4h left well\n')
    file.write(f'x_offset = {x_offset} px\n')
    file.write(f'y_offset = {y_offset} px\n\n')

# 4 loops for frames, columns and rows of original tif
for h in range(fr_series):    # frames
    for i in range(cols):      # cols
        for j in range(rows):   # rows
            # 'test_set' and 'subdir' are used to split into test/train set
            subdir = ''
            test_set = (i == 0 and (j in [0, 5])) or (i == 1 and (j in [1, 6])) or (i == 2 and (j in [2, 7])) or (i == 3 and (j in [3, 8])) or (i == 4 and (j in [4, 9])) or (i == 5 and (j in [5, 10])) or (
                i == 6 and (j in [6, 11])) or (i == 7 and (j in [7, 12])) or (i == 8 and j == 8) or (i == 9 and j == 9) or (i == 10 and j == 10) or (i == 11 and j == 11) or (i == 12 and j == 12)
            if test_set:
                subdir = 'test'
            else:
                subdir = 'train'

            # select the first or last 48 frames
            fr_range = (0, 0)
            if (counter % 2) == 0:
                fr_range = (0, 48)
            elif (counter % 2) == 1:
                fr_range = (24, 72)

            # select the current_tif
            current_tif = left_well[fr_range[0]:fr_range[1], y_offset +
                                    512*j:y_offset+512*(j+1), x_offset+512*i:x_offset+512*(i+1)]
            counter += 1
            print(
                f'{fr_range[0]}:{fr_range[1]}, {y_offset+512*j}:{y_offset+512*(j+1)}, {x_offset+512*i}:{x_offset+512*(i+1)}')

            # create folder for video with respecting video number
            video_num, test_video_num, train_video_num = setVideoNums(
                subdir, test_video_num, train_video_num)
            video_num_str = genNumStr(video_num)
            foldername = f'video_{video_num_str}'
            folderpath = os.path.join(dir, subdir, foldername)
            os.mkdir(folderpath)
            # note details of the current video in the overview file
            with open(overview_file_path, 'a') as file:
                file.write(
                    f'video_{video_num_str} (ori) in {subdir}: column{i}, row{j}, frames {fr_range[0]}-{fr_range[1]}\n')
            print(f'{subdir} video_{video_num_str} saved.')
            # increase video number
            video_num, test_video_num, train_video_num = setVideoNums(
                subdir, test_video_num, train_video_num, increase=True)
            video_num_str = genNumStr(video_num)

            if False:
                # save the rotated videos for the selected column and row in the test set
                subdir = 'test'
            # create folder for the rotated video with respective video number
            video_num, test_video_num, train_video_num = setVideoNums(
                subdir, test_video_num, train_video_num)
            video_num_str = genNumStr(video_num)
            foldername_rot = f'video_{video_num_str}'
            folderpath_rot = os.path.join(dir, subdir, foldername_rot)
            os.mkdir(folderpath_rot)
            # note details to the current video in the overview file
            with open(overview_file_path, 'a') as file:
                file.write(
                    f'video_{video_num_str} (rot) in {subdir}: column{i}, row{j}, frames {fr_range[0]}-{fr_range[1]}\n')
            print(f'{subdir} video_{video_num_str} saved.')
            # increase the video number
            video_num, test_video_num, train_video_num = setVideoNums(
                subdir, test_video_num, train_video_num, increase=True)
            video_num_str = genNumStr(video_num)

            # finally: save original and rotated frames in the respective folders
            for frame in range(0, 48, 4):
                current_frame = current_tif[frame]
                frame_name = frame//4
                frame_str = genNumStr(frame_name, digits=2)
                filename = f'frame_{frame_str}.jpg'
                filepath = os.path.join(folderpath, filename)
                tiff.imwrite(filepath, current_frame)
                img_original = Image.open(filepath)
                img_rot = img_original.rotate(90)
                filepath_rot = os.path.join(folderpath_rot, filename)
                img_rot.save(filepath_rot)

print(f'\nFinal counter: {counter}')
