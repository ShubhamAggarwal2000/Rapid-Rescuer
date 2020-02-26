import tensorflow as tf
import cv2
import numpy as np
import math
from scipy import ndimage

digit_loc = []
img_arr = []
CELL_SIZE = 40
def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty
def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted


def readImage(img_file_path):
    img1 = cv2.imread(img_file_path)
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    return binary_img


img_file_path = 'practice_maze.jpg'

rows = 10
cols = 10


def maze_iso(img):
    global rows
    global cols
    global digit_loc
    d1 = 0
    for y in range(20, 40 * (rows), 40):
        for x in range(20, 40 * (cols), 40):
            t = 0
            for i in range(x - 16, x + 16, 1):
                t += img[i][y]
            if (t != 8160):
                digit_loc.append((x, y))
                d1 = d1 + 1
    temp = np.zeros([16, 16], dtype=int)
    for y in range(0, d1):
        temp = img[(digit_loc[y][0] - 16):(digit_loc[y][0] + 16), (digit_loc[y][1] - 16):(digit_loc[y][1] + 16)]

        temp = cv2.resize(255-temp , (28,28))

        gray = temp/255.0
        while np.sum(gray[0]) == 0:
            gray = gray[1:]

        while np.sum(gray[:,0]) == 0:
            gray = np.delete(gray,0,1)

        while np.sum(gray[-1]) == 0:
            gray = gray[:-1]

        while np.sum(gray[:,-1]) == 0:
            gray = np.delete(gray,-1,1)

        rows,cols = gray.shape
        if rows > cols:
            factor = 20.0/rows
            rows = 20
            cols = int(round(cols*factor))
            gray = cv2.resize(gray, (cols,rows))
        else:
            factor = 20.0/cols
            cols = 20
            rows = int(round(rows*factor))
            gray = cv2.resize(gray, (cols, rows))
        colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
        rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
        gray = np.pad(gray,(rowsPadding,colsPadding),'constant' ,constant_values =0)    
        shiftx,shifty = getBestShift(gray)
        shifted = shift(gray,shiftx,shifty)
        gray = shifted
        img_arr.append(gray)
        str1 = 'temp' + str(y)
    return img_arr

bin_img = readImage(img_file_path)
final = maze_iso(bin_img)
img_arr = np.array(img_arr)

cv2.waitKey(0)
cv2.destroyAllWindows()

model = tf.keras.models.load_model("eyantra_img.model")
digit_list = []
for i in img_arr:
    i = i.reshape((1,28,28,1))
    predict = model.predict(i)
    digit_list.append(np.argmax(predict))

print(digit_list)

    
