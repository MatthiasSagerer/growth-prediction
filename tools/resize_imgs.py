
from itertools import tee
from logging import root
from pickle import FALSE
import cv2
import os
import sys

project_path = os.getcwd()
print(project_path)
sys.path.append(project_path)
from tools.calc_duration import currentDateTime, calculateDuration
from tools.disp_mult_img import imreadRelPath, dispImgs


# Create resized Dataset of Dataset1/2: 128x128, 256x256, 512x512
dataset_path = os.path.join(
    os.getcwd(), 'resources', 'data', 'growth_pred_Dataset1_and_2')
test_path = os.path.join(dataset_path, 'test')
train_path = os.path.join(dataset_path, 'train')


def listDirContents(dir):
    for i, folder in enumerate(os.listdir(test_path)):
        print(folder)


def resizeImgs(old_path, new_rel_path, size):
    for i, folder in enumerate(os.listdir(old_path)):
        print(f'{i}. folder: {folder}')
        new_folder_path = os.path.join(os.getcwd(), new_rel_path, folder)
        os.mkdir(new_folder_path)
        folder_path = os.path.join(old_path, folder)
        for i, file in enumerate(os.listdir(folder_path)):
            old_file_path = os.path.join(old_path, folder, file)
            new_file_path = os.path.join(new_rel_path, folder, file)
            img_rel_path = os.path.join(old_path, folder, file)
            img = imreadRelPath(img_rel_path)
            img_resized = cv2.resize(
                img, (size, size), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(new_file_path, img_resized)

            # print(f'---{i}. file:{file}')
            # dispImgs([img, img_resized], millisecs=125)
            # print(old_file_path)
            # print(new_file_path)


#####################################
'''
FOLDER NAMES HAVE TO BE ADJUSTED BEFORE EXECUTION

REMOVE FALSE TO EXECUTE CODE
'''
#####################################

if __name__ == '__main__' and FALSE:
    start = currentDateTime('Start code execution')
    print(f'{start[0]}\n\n\n')

    dataset_path = os.path.join(
        os.getcwd(), 'resources', 'data', 'growth_pred_Dataset1_and_2')
    dataset_rel_path = os.path.join(
        'resources', 'data', 'growth_pred_Dataset1_and_2')

    test_path = os.path.join(dataset_path, 'test')
    train_path = os.path.join(dataset_path, 'train')

    # listDirContents(dataset_path)

    test_512_rel_path = os.path.join(dataset_rel_path, 'test_512')
    test_256_rel_path = os.path.join(dataset_rel_path, 'test_256')
    test_128_rel_path = os.path.join(dataset_rel_path, 'test_128')

    train_512_rel_path = os.path.join(dataset_rel_path, 'train_512')
    train_256_rel_path = os.path.join(dataset_rel_path, 'train_256')
    train_128_rel_path = os.path.join(dataset_rel_path, 'train_128')

    # resizeImgs(test_path, test_512_rel_path, 512)
    # resizeImgs(test_path, test_256_rel_path, 256)
    # resizeImgs(test_path, test_128_rel_path, 128)

    resizeImgs(train_path, train_512_rel_path, 512)
    resizeImgs(train_path, train_256_rel_path, 256)
    resizeImgs(train_path, train_128_rel_path, 128)

    end = currentDateTime('\n\nEnd code execution')
    print(end[0])
    duration = calculateDuration(start[1], end[1])
    print(f'Training duration: {duration}')
