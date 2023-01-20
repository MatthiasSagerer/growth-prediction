# 7 columns, 13 rows => 91 cutouts
# 91 cutouts mirrored on the vertical axis => 182 cutouts
# 2 12 FrVi per cutout => 364 vids
# 42 test vids, 322 train vids

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
# right_well = tiff.imread(os.path.join(source_dir, '03_right_well_72frames.tif'))

# segmented
right_well = tiff.imread(os.path.join(
    source_dir, '07_right_well_auto_threshold.tif'))

# find edges
# right_well = tiff.imread(os.path.join(source_dir, '04_right_well_find_edges_72fr.tif'))

x_offset = 0
y_offset = 0
fr_series = 2
cols = 7
rows = 13
video_num = 0
test_video_num = 42
train_video_num = 322

# select directory to save the processed frames
target_dir = 'P:/BaTh/Dataset4_22-04-22/dataAug'

# original
dir = os.path.join(target_dir, 'mir')

# create test/train folder and overview file
# os.mkdir(os.path.join(dir, 'train'))
# os.mkdir(os.path.join(dir, 'test'))
overview_file_path = os.path.join(dir, 'mir_overview_right_well.txt')
with open(overview_file_path, 'w') as file:
    file.write('File overview for mir right well\n')
    file.write(f'x_offset = {x_offset} px\n')
    file.write(f'y_offset = {y_offset} px\n\n')

# 4 loops for frames, columns and rows of original tif
for h in range(fr_series):    # frames
    for i in range(cols):      # cols
        for j in range(rows):   # rows
            # 'test_set' and 'subdir' are used to split into test/train set
            subdir = ''
            test_set = (i == 0 and j == 0) or (i == 1 and j == 1) or (i == 2 and j == 2) or (i == 3 and (j in [3, 9])) or (
                i == 4 and (j in [4, 10])) or (i == 5 and (j in [5, 11])) or (i == 6 and j == 6) or (i == 6 and j == 12 and h == 0)
            if test_set:
                subdir = 'test'
            else:
                subdir = 'train'

            # select the current_tif
            current_tif = right_well[36*h:36*(h+1), y_offset+512*j:y_offset+512*(
                j+1), x_offset+512*i:x_offset+512*(i+1)]
            # print(f'{36*h}:{36*(h+1)}, {y_offset+512*j}:{y_offset+512*(j+1)}, {x_offset+512*i}:{x_offset+512*(i+1)}')

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
                    f'video_{video_num_str} (ori) in {subdir}: column{i}, row{j}, frames {36*h+1}-{36*(h+1)}\n')
            print(f'{subdir} video_{video_num_str} saved.')
            # increase video number
            video_num, test_video_num, train_video_num = setVideoNums(
                subdir, test_video_num, train_video_num, increase=True)
            video_num_str = genNumStr(video_num)

            # create folder for the mirrored video with respective video number
            video_num, test_video_num, train_video_num = setVideoNums(
                subdir, test_video_num, train_video_num)
            video_num_str = genNumStr(video_num)
            foldername_mir = f'video_{video_num_str}'
            folderpath_mir = os.path.join(dir, subdir, foldername_mir)
            os.mkdir(folderpath_mir)
            # note details to the current video in the overview file
            with open(overview_file_path, 'a') as file:
                file.write(
                    f'video_{video_num_str} (mir) in {subdir}: column{i}, row{j}, frames {36*h+1}-{36*(h+1)}\n')
            print(f'{subdir} video_{video_num_str} saved.')
            # increase the video number
            video_num, test_video_num, train_video_num = setVideoNums(
                subdir, test_video_num, train_video_num, increase=True)
            video_num_str = genNumStr(video_num)

            # finally: save original and mirrored frames in the respective folders
            for frame in range(0, 36, 3):
                current_frame = current_tif[frame]
                frame_name = frame//3
                frame_str = genNumStr(frame_name, digits=2)
                filename = f'frame_{frame_str}.jpg'
                filepath = os.path.join(folderpath, filename)
                tiff.imwrite(filepath, current_frame)
                img_original = Image.open(filepath)
                img_mir = img_original.transpose(
                    Image.Transpose.FLIP_LEFT_RIGHT)
                filepath_mir = os.path.join(folderpath_mir, filename)
                img_mir.save(filepath_mir)
