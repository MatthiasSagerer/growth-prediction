import cv2
import numpy as np

ori_path = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg_datasets/ori_1h/train/video_000/frame00.jpg'
edg_path = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg_datasets/edg_1h/train/video_000/frame00.jpg'
seg_path = 'P:/BaTh/Dataset4_22-04-22/tIntervSeg_datasets/seg_1h/train/video_000/frame00.jpg'

ori_img = cv2.imread(ori_path)
edg_img = cv2.imread(edg_path)
seg_img = cv2.imread(seg_path)

ori_img = cv2.resize(ori_img, (384, 384))
edg_img = cv2.resize(edg_img, (384, 384))
seg_img = cv2.resize(seg_img, (384, 384))

border = np.full((384, 5, 3), (127, 127, 127), dtype=np.uint8)
stack = (ori_img, border, edg_img, border, seg_img)
stack_img = np.hstack(stack)

# cv2.imshow('img', stack_img)
# cv2.waitKey(0)

# cv2.imwrite('C:/Users/Matthias Sagerer/Downloads/tIntervSeg_vid_000_fr00.png', stack_img)
