# Target of preprocessing (resolution: 7168x6656):
# 728 videos (resolution: 512x512) with 12 frames each := 12FrVi

'''
NOTE: When selecting "current_tif", columns and rows are switched by accident.
      Because this doesn't change the nature of the desired dataset this mistake
      wasn't fixed.
'''

from distutils.util import subst_vars
from doctest import testfile
from inspect import currentframe
from cv2 import rotate
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
# right_well = tiff.imread(os.path.join(source_dir, '07_right_well_auto_threshold.tif'))

# find edges
# right_well = tiff.imread(os.path.join(source_dir, '04_right_well_find_edges_72fr.tif'))

x_offset = 512
y_offset = 512
fr_series = 6
cols = 4
rows = 8
video_num = 0
test_video_num = 42
train_video_num = 322

# select directory to save the processed frames
target_dir = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg'

# original
# dir = os.path.join(target_dir, 'ori_1h')

# segmented
# dir = os.path.join(target_dir, 'seg_1h')

# find edges
# dir = os.path.join(target_dir, 'edg_1h')

# test/train folder already created for right well
# os.mkdir(os.path.join(dir, 'train'))
# os.mkdir(os.path.join(dir, 'test'))
overview_file_path = os.path.join(dir, '1h_overview_right_well.txt')
with open(overview_file_path, 'w') as file:
    file.write('File overview for 1h right well\n')
    file.write(f'x_offset = {x_offset} px\n')
    file.write(f'y_offset = {y_offset} px\n\n')

# 4 loops for frames, columns and rows of original tif
for h in range(fr_series):    # frames
    for i in range(cols):      # columns
        for j in range(rows):   # rows
            if (i == 3 and j == 5) or ((h == 0 or h == 1 or h == 4 or h == 5) and j == 7 and i == 3):
                # these frames get skipped to have a consistent size for all data sets
                print(
                    f'frames {12*h+1}-{12*(h+1)}, column {i}, row {j} are skipped')
            else:
                # 'test_set' and 'subdir' are used to split into test/train set
                subdir = ''
                test_set = (i == 0 and j == 0) or (
                    i == 1 and j == 2) or (i == 2 and j == 4)
                if test_set:
                    subdir = 'test'
                else:
                    subdir = 'train'
                # select the current_tif
                current_tif = right_well[12*h:12*(h+1), x_offset+512*i:x_offset+512*(
                    i+1), y_offset+512*j:y_offset+512*(j+1)]
                '''Here, when accessing the right_well, the rows and columns are switched.'''

                # create folder for video with respective video number
                video_num, test_video_num, train_video_num = setVideoNums(
                    subdir, test_video_num, train_video_num)
                video_num_str = genNumStr(video_num)
                foldername = f'video_{video_num_str}'
                folderpath = os.path.join(dir, subdir, foldername)
                os.mkdir(folderpath)
                # note details of the current video in the overview file
                with open(overview_file_path, 'a') as file:
                    file.write(
                        f'video_{video_num_str} (ori) in {subdir}: column{i}, row{j}, frames {12*h+1}-{12*(h+1)}\n')
                print(f'{subdir} video_{video_num_str} saved.')
                # increase video number
                video_num, test_video_num, train_video_num = setVideoNums(
                    subdir, test_video_num, train_video_num, increase=True)
                video_num_str = genNumStr(video_num)

                if (i == 3 and j == 6):
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
                        f'video_{video_num_str} (rot) in {subdir}: column{i}, row{j}, frames {12*h+1}-{12*(h+1)}\n')
                print(f'{subdir} video_{video_num_str} saved.')
                # increase the video number
                video_num, test_video_num, train_video_num = setVideoNums(
                    subdir, test_video_num, train_video_num, increase=True)
                video_num_str = genNumStr(video_num)

                # finally: save original and rotated frames in the respective folders
                for frame in range(12):
                    current_frame = current_tif[frame]
                    frame_str = genNumStr(frame, digits=2)
                    filename = f'frame_{frame_str}.jpg'
                    filepath = os.path.join(folderpath, filename)
                    tiff.imwrite(filepath, current_frame)
                    img_original = Image.open(filepath)
                    img_rot = img_original.rotate(90)
                    filepath_rot = os.path.join(folderpath_rot, filename)
                    img_rot.save(filepath_rot)
