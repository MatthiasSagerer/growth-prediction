import cv2
import numpy as np


margin = 15
thick = 50
gap = 5
length = 4
space = 75
captions = 75

width = 10000
height = int(2*margin+captions + 3*(2*gap+(4*thick)//3)+2*(thick+gap)+thick//3)


def addLoopBlock(img, pos=(0, 0), inner=3, color=(255, 0, 0), ret_w=False):
    img_copy = img.copy()
    x_pos = pos[0]
    y_pos = pos[1]
    add_width = int(inner * (gap + thick//3))
    pts_top = [(x_pos, y_pos),
               (int(x_pos+thick*length)+add_width, y_pos+thick)]
    pts_mid = [(x_pos, y_pos+thick),
               (int(x_pos+thick//3), int(y_pos+inner*(2*gap+(4*thick)//3)+2*(thick+gap)))]
    pts_bot = [(x_pos, int(y_pos+inner*(2*gap+(4*thick)//3)+2*(thick+gap))),
               (int(x_pos+thick*length)+add_width, int(y_pos+inner*(2*gap+(4*thick)//3)+2*(thick+gap)+thick//3))]
    cv2.rectangle(img_copy, pts_top[0], pts_top[1], color, cv2.FILLED)
    cv2.rectangle(img_copy, pts_mid[0], pts_mid[1], color, cv2.FILLED)
    cv2.rectangle(img_copy, pts_bot[0], pts_bot[1], color, cv2.FILLED)

    if ret_w:
        return img_copy, int(x_pos+thick*length)+add_width

    return img_copy


def bPos(ori_pos, level):
    new_x = int(ori_pos[0] + level*(thick//3 + gap))
    new_y = ori_pos[1] + level*(thick+gap)
    return (new_x, new_y)


fig = np.zeros((height, width, 3), np.uint8)
fig[:] = 255
blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)

# GeoDataViz Colour Palettes
col1 = tuple(reversed((175, 88, 186)))
col2 = tuple(reversed((255, 199, 30)))
col3 = tuple(reversed((255, 31, 91)))
col4 = tuple(reversed((0, 155, 222)))
col5 = tuple(reversed((0, 205, 108)))
col6 = tuple(reversed((242, 135, 34)))
col7 = tuple(reversed((166, 118, 29)))


origin1 = (margin, margin+captions)
# colors1 = [red, blue, green, red, green]
colors1 = [col1, col2, col3, col4, col5]
fig = addLoopBlock(fig, pos=origin1, inner=3, color=colors1[0])
fig = addLoopBlock(fig, pos=bPos(origin1, 1), inner=2, color=colors1[1])
fig = addLoopBlock(fig, pos=bPos(origin1, 2), inner=1, color=colors1[2])
fig = addLoopBlock(fig, pos=bPos(origin1, 3), inner=0, color=colors1[3])
rec_pos = bPos(origin1, 4)
cv2. rectangle(fig, rec_pos, (int(
    rec_pos[0]+thick*length-thick//3-gap), rec_pos[1]+thick), colors1[4], cv2.FILLED)

origin2 = (int(origin1[0]+thick*length+3 *
           (gap+thick//3))+space, margin+captions)
color2 = red
color2 = col6
fig = addLoopBlock(fig, pos=origin2, inner=2, color=color2)
fig = addLoopBlock(fig, pos=bPos(origin2, 1), inner=1, color=colors1[2])
fig = addLoopBlock(fig, pos=bPos(origin2, 2), inner=0, color=colors1[3])
rec_pos = bPos(origin2, 3)
cv2. rectangle(fig, rec_pos, (int(
    rec_pos[0]+thick*length-thick//3-gap), rec_pos[1]+thick), colors1[4], cv2.FILLED)

origin3 = (int(origin2[0]+thick*length+2 *
           (gap+thick//3))+space, margin+captions)
color3 = green
color3 = col7
fig = addLoopBlock(fig, pos=origin3, inner=2, color=color3)
fig = addLoopBlock(fig, pos=bPos(origin3, 1), inner=1, color=colors1[2])
fig = addLoopBlock(fig, pos=bPos(origin3, 2), inner=0, color=colors1[3])
rec_pos = bPos(origin3, 3)
cv2. rectangle(fig, rec_pos, (int(
    rec_pos[0]+thick*length-thick//3-gap), rec_pos[1]+thick), colors1[4], cv2.FILLED)

new_width = addLoopBlock(fig, pos=bPos(origin3, 2),
                         inner=0, color=colors1[2], ret_w=True)[1] + margin

print(fig.shape)
fig = np.delete(fig, [i for i in range(new_width, fig.shape[1]-1)], 1)
print(fig.shape)

# cv2.imwrite('C:/Users/Matthias Sagerer/Downloads/analysis_procedure.png', fig)

cv2.imshow('Figure', fig)
cv2.moveWindow('Figure', 1950, 0)
cv2.waitKey(0)
