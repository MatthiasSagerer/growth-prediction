import sys
from turtle import pd, width
from venv import create
import cv2
import time
import math
import os
from tkinter import Tk, messagebox

# create correct path for linux/windows
def createPath(relativePath):
    platf = sys.platform
    if platf == 'win32':
        return relativePath
    elif platf == 'linux' or platf == 'linux2':
        project_dir = 'py-opencv/'
        cwd = os.getcwd()
        cwd = cwd.split('py-opencv/')[0]
        if cwd[-10:] == '/py-opencv': project_dir = ''
        total_path = os.path.join(cwd, project_dir, relativePath)
        return total_path

# read image with path relative to "py-opencv"
def imreadRelPath(relative_path):
    return cv2.imread(createPath(relative_path))

# show positioned image
def showPosImg(img_list, millisecs, coords=[[0, 0]]):
    wins = [f'window {i + 1}' for i in range(len(img_list))]
    for i in range(len(img_list)):
        cv2.namedWindow(wins[i])
        cv2.moveWindow(wins[i], coords[i][0], coords[i][1])
        cv2.imshow(wins[i], img_list[i])
    cv2.waitKey(millisecs)
  
# return screen-width/-height as tuple   
def getScreensize():
    root_win = Tk()
    root_win.withdraw()
    screen_size = (root_win.winfo_screenwidth(), root_win.winfo_screenheight())
    return screen_size

# display one image on the screen
def showOneImg(img_list, screensize, margin, millisecs):
    img = img_list[0]
    screen_width = screensize[0]
    screen_height = screensize[1]
    w = img.shape[1]
    h = img.shape[0]
    if w > screen_width - 5*margin:
        w = screen_width - 5*margin
        h = math.floor(w * img.shape[0]/img.shape[1])
    if h > screen_height - 5*margin:
        h = screen_height - 5*margin
        w = math.floor(h * img.shape[1]/img.shape[0])
    resized_img = cv2.resize(img, (w, h))
    showPosImg([resized_img], millisecs)

# display two imaged on the screen
def showTwoImg(img_list, screenheight, half_screen_width, margin, millisecs):
    img1 = img_list[0]
    img2 = img_list[1]
    x1 = math.floor(0.75*margin)
    x2 = math.floor(half_screen_width + 0.5*margin)
    y = math.floor(margin)
    w = math.floor(half_screen_width - margin)
    h = math.floor(screenheight - 5.5*margin)
    if w < img1.shape[1]: 
        w1 = w
    else:
        w1 = img1.shape[1]
    if w < img2.shape[1]:
        w2 = w
    else:
        w2 = img2.shape[1]
    h1 = math.floor(w1 * img1.shape[0]/img1.shape[1])
    h2 = math.floor(w2 * img2.shape[0]/img2.shape[1])
    if h1 > h:
        h1 = h
        w1 = math.floor(h1 * img1.shape[1]/img1.shape[0])
    if h2 > h:
        h2 = h
        w2 = math.floor(h2 * img2.shape[1]/img2.shape[0])
    img1_resized = cv2.resize(img1, (w1, h1))
    img2_resized = cv2.resize(img2, (w2, h2))
    coords = [[x1, y], [x2, y]]
    showPosImg([img1_resized, img2_resized], millisecs, coords)
  
# display three/four images on the screen  
def showThreeOrFourImg(img_list, half_screen_width, half_screen_height, margin, millisecs):
    x1 = math.floor(0.75*margin)
    x2 = math.floor(half_screen_width)
    y1 = 0
    y2 = math.floor(half_screen_height - 1.25*margin)
    widths = []
    heights = []
    for i in range(len(img_list)):
        height_i = math.floor(half_screen_height - 3*margin)
        if img_list[i].shape[0] < height_i: height_i = img_list[i].shape[0]
        heights.append(height_i)
    for i in range(len(img_list)):
        width_i = math.floor(heights[i] * img_list[i].shape[1]/img_list[i].shape[0])
        if img_list[i].shape[1] < width_i: width_i = img_list[i].shape[1]
        widths.append(width_i)
    w = math.floor(half_screen_width - margin)
    for i in range(len(img_list)):
        if widths[i] >= w:
            widths[i] = w
            heights.append(math.floor(w * img_list[i].shape[0]/img_list[i].shape[1]))
    imgs_resized = []
    for i in range(len(img_list)):
        imgs_resized.append(cv2.resize(img_list[i], (widths[i], heights[i])))
    if len(img_list) == 3:
        coords = [[x1, y1], [x2, y1], [x1, y2]]
    elif len(img_list) == 4:
        coords = [[x1, y1], [x2, y1], [x1, y2], [x2, y2]]
    showPosImg(imgs_resized, millisecs, coords)

# display more than four but less then 250 images on the screen
def showManyImg(img_list, screensize, margin, millisecs):
    screen_width = screensize[0]
    screen_height = screensize[1]
    resized_img_list = []
    target_shape = (math.floor(screen_width - 10*margin), math.floor(screen_height - 10*margin))
    for image in img_list:
        if image.shape[1] > target_shape[0] or image.shape[0] > target_shape[1]:
            width = target_shape[0]
            height = math.floor(screen_height * image.shape[0]/image.shape[1])
            if height > target_shape[1]:
                height = target_shape[1]
                width = math.floor(height * image.shape[1]/image.shape[0])
            else:
                height = image.shape[0]
            resized_img_list.append(cv2.resize(image, (width, height)))
        else:
            resized_img_list.append(image)
    half_margin = math.floor(3*margin)
    coords = [(half_margin, half_margin) for i in range(len(img_list))]
    showPosImg(resized_img_list, millisecs, coords)

# display an arbitrary amount of images on the screen
def dispImgs(img_list, millisecs=0):
    img_limit = 250
    screensize = getScreensize()
    half_screen_width = screensize[0]/2
    margin = 20
    if len(img_list) == 0:
        root_win = Tk()
        root_win.withdraw()
        err_msg = 'No image to show was passed.'
        messagebox.showerror('Error', err_msg)
    elif len(img_list) == 1:
        showOneImg(img_list, screensize, margin, millisecs)
    elif len(img_list) == 2:
        showTwoImg(img_list, screensize[1], half_screen_width, margin, millisecs)
    elif len(img_list) == 3 or len(img_list) == 4:
        showThreeOrFourImg(img_list, half_screen_width, screensize[1]/2, margin, millisecs)
    elif len(img_list) > 4 and len(img_list) <= img_limit:
        showManyImg(img_list, screensize, margin, millisecs)
    else:
        root_win = Tk()
        root_win.withdraw()
        err_msg = f'''{len(img_list)} images to show, which exceeds the limits of {img_limit} images.
Select fewer images or adjust the limit.'''
        messagebox.showerror('Error', err_msg)
    cv2.destroyAllWindows()

def main():
    print('The file "disp_mult_img.py" was executed.')   

if __name__ == '__main__':
    main()