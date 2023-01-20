import os
import cv2
import numpy as np

video_path = 'P:/BaTh/Dataset4_22-04-22/dataSframeR_datasets/original/test_660px/frames01'

frs_names = os.listdir(video_path)
frs_paths = [os.path.join(video_path, frame)
             for i, frame in enumerate(frs_names[:12])]
frs = [cv2.imread(path) for i, path in enumerate(frs_paths)]

# for i, fr in enumerate(frs):
#     cv2.imshow(f'frame {i+1}', fr)
#     cv2.waitKey(0)

# create new list with border
w_hborder = 5
h_vborder = 10
border_col = (127, 127, 127)
stack_list = []
for i in range(22):
    if i in (1, 3, 5, 7, 9, 12, 14, 16, 18, 20):
        hborder = np.full((128, w_hborder, 3), border_col, dtype=np.uint8)
        stack_list.append(hborder)
    else:
        img = frs.pop(0)
        img_res = cv2.resize(img, (128, 128))
        stack_list.append(img_res)

first_row = np.hstack(tuple(stack_list[:11]))
second_row = np.hstack(tuple(stack_list[11:]))

w_vborder = 6*128 + 5*w_hborder
vborder = np.full((h_vborder, w_vborder, 3), border_col, dtype=np.uint8)
both_rows = np.vstack((first_row, vborder, second_row))

# cv2.imshow('first row', first_row)
# cv2.imshow('second row', second_row)
# cv2.imshow('img', both_rows)
# cv2.waitKey(0)

cv2.imwrite(
    'C:/Users/Matthias Sagerer/Downloads/dataSframeR_video2.png', both_rows)
