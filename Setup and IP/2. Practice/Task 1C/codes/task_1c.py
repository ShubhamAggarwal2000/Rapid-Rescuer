
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1C of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1c.py
# Functions:		computeSum
# 					[ Comma separated list of functions in this file ]
# Global variables:	None
# 					[ List of global variables defined in this file ]


# Import necessary modules
import cv2
import numpy as np
import os
import sys
import math


#############	You can import other modules here	#############
import tensorflow as tf
curr_dir_path = os.getcwd()
task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
sys.path.append(task_1a_dir_path)

import task_1a
curr_dir_path = os.getcwd()
img_dir_path = curr_dir_path + '/../task_1c_images/'				# path to directory of 'task_1c_images'

file_num = 0
img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file
original_binary_img = task_1a.readImage(img_file_path)
height, width = original_binary_img.shape
task_1a.CELL_SIZE = 40
no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
initial_point = (0, 0)											# start point coordinates of maze
final_point = ((no_cells_height-1),(no_cells_width-1))
count=0


#################################################################


# Function Name:	computeSum
# Inputs: 			img_file_path [ file path of image ]
# 					shortestPath [ list of coordinates of shortest path from initial_point to final_point ]
# Outputs:			digits_list [ list of digits present in the maze image ]
# 					digits_on_path [ list of digits present on the shortest path in the maze image ]
# 					sum_of_digits_on_path [ sum of digits present on the shortest path in the maze image ]
# Purpose: 			the function takes file path of original image and shortest path in the maze image
# 					to return the list of digits present in the image, list of digits present on the shortest
# 					path in the image and sum of digits present on the shortest	path in the image
# Logic:			[ write the logic in short of how this function solves the purpose ]
# Example call: 	digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

def computeSum(img_file_path, shortestPath):

    """
    Purpose:
    ---
    the function takes file path of original image and shortest path as argument and returns list of digits, digits on path and sum of digits on path

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image
    `shortestPath` :		[ list ]
        list of coordinates of shortest path from initial_point to final_point

    Returns:
    ---
    `digits_list` :	[ list ]
        list of all digits on image
    `digits_on_path` :	[ list ]
        list of digits adjacent to the path from initial_point to final_point
    `sum_of_digits_on_path` :	[ int ]
        sum of digits on path

    Example call:
    ---
    original_binary_img = readImage(img_file_path)

    """

    digits_list = []
    digits_on_path = []
    coordinate_of_num1 = []
    coor_num_on_path=[]
    coor_num_on_path1=[]
    sum_of_digits_on_path = 0
    img = readImage(img_file_path)
    digit_img_array, coordinate_of_num = maze_iso(img)
    #print(coordinate_of_num)
    #print(len(coordinate_of_num))
    for i in range(0,len(coordinate_of_num)):
            #print(i)
            #print(coordinate_of_num[i])
            (x1,y1)=(int((coordinate_of_num[i][0]-20)/40), int((coordinate_of_num[i][1]-20)/40))
            #print(x1,y1)
            coordinate_of_num1.append((x1,y1))
    #print(coordinate_of_num1)
    #print(shortestPath)
    coor_num_on_path1 = compare(shortestPath, coordinate_of_num1, img)
    for i in range(0,len(coor_num_on_path1)):
            #print(i)
            #print([i])
            (x1,y1)=(int((coor_num_on_path1[i][0]*40)+20), int((coor_num_on_path1[i][1]*40)+20))
            #print(x1,y1)
            coor_num_on_path.append((x1,y1))
    #print(coor_num_on_path)
    for i in range(len(digit_img_array)):
        #cv2.imshow("heeee",digit_img_array[i])
        #cv2.waitKey(0)
        im1 = img[(coordinate_of_num[i][0] - 16):(coordinate_of_num[i][0] + 16),
             (coordinate_of_num[i][1] - 16):(coordinate_of_num[i][1] + 16)]
        temp2=digit_recog(im1)
        digits_list.append(int(temp2))
    #print(digits_list)
    for i in range(len(coor_num_on_path)):
        im = img[(coor_num_on_path[i][0] - 16):(coor_num_on_path[i][0] + 16),
             (coor_num_on_path[i][1] - 16):(coor_num_on_path[i][1] + 16)]
        temp1 = digit_recog(im)
        digits_on_path.append(int(temp1))
        sum_of_digits_on_path += int(temp1)
    ###################################################

    return digits_list, digits_on_path, sum_of_digits_on_path


#############	You can add other helper functions here		#############



# def check_boundary(img,num_on_path,path):
# 	for i in range(len(num_on_path)):
# 		if


def compare(path, num, img):
    shortestPath=path
    inner_path = []
    outer_path = []
    num_on_path=[]
    for i in range(0, len(shortestPath) - 1):
        if shortestPath[i][0] == shortestPath[i + 1][0]:
            incell = (shortestPath[i][0] + 1, shortestPath[i][1])
            outcell1 = (shortestPath[i][0] - 1, shortestPath[i][1])
            outcell2 = (shortestPath[i + 1][0] - 1, shortestPath[i + 1][1])
            if incell not in inner_path:
                inner_path.append(incell)
            if outcell1 not in outer_path:
                outer_path.append(outcell1)
            if outcell2 not in outer_path:
                outer_path.append(outcell2)
        if shortestPath[i][1] == shortestPath[i + 1][1]:
            incell = (shortestPath[i + 1][0], shortestPath[i + 1][1] - 1)
            outcell1 = (shortestPath[i + 1][0], shortestPath[i + 1][1] + 1)
            outcell2 = (shortestPath[i][0], shortestPath[i][1] + 1)
            if incell not in inner_path:
                inner_path.append(incell)
            if outcell1 not in outer_path:
                outer_path.append(outcell1)
            if outcell2 not in outer_path:
                outer_path.append(outcell2)
    l = len(shortestPath)
    #print(shortestPath[l - 1])
    endi = (shortestPath[l - 1][0], shortestPath[l - 1][1] + 1)
    #print(inner_path)
    outi = (shortestPath[l - 1][0] + 1, shortestPath[l - 1][1])
    #print(outer_path)
    inner_path.append(outi)
    outer_path.append(endi)
    #print(num)
    for i in range(0,len(num)):
        if num[i] in inner_path:
            num_on_path.append(num[i])
        elif num[i] in outer_path:
            num_on_path.append(num[i])
   # print("num on path",num_on_path)
    matrixx = task_1a.Maze_matrix(original_binary_img, no_cells_height, no_cells_width)
    #print(matrixx)
    keep1=[]
    #print(len(num_on_path))
    for i in range(len(num_on_path)):
        if (num_on_path[i][0]-1,num_on_path[i][1]) in shortestPath:
           # print("for point", i, "path is up")
            if matrixx[2*(num_on_path[i][0])][2*(num_on_path[i][1])+1]==0:
                keep1.append((num_on_path[i][0],num_on_path[i][1]))
                #print("for point", i, "path is up is kept")
        if (num_on_path[i][0]+1,num_on_path[i][1]) in shortestPath:
           # print("for point", i, "path is down")
            if matrixx[2*(num_on_path[i][0])+2][2*(num_on_path[i][1])+1]==0:
                keep1.append((num_on_path[i][0],num_on_path[i][1]))
               # print("for point", i, "path is down is kept")
        if (num_on_path[i][0],num_on_path[i][1]-1) in shortestPath:
           # print("for point", i, "path is left")
            if matrixx[2*(num_on_path[i][0])+1][2*(num_on_path[i][1])]==0:
                keep1.append((num_on_path[i][0],num_on_path[i][1]))
                #print("for point", i, "path is left is kept")
        if (num_on_path[i][0],num_on_path[i][1]+1) in shortestPath:
           # print("for point", i, "path is right")
            if matrixx[2*(num_on_path[i][0])+1][2*(num_on_path[i][1])+2]==0:
                keep1.append((num_on_path[i][0],num_on_path[i][1]))
                #print("for point", i, "path is right is kept")
    #print("number to keep",keep)
    return keep1


def readImage(img_file_path):
    img1 = cv2.imread(img_file_path)
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    return binary_img


def maze_iso(img):
    coordinate_of_num=[]
    img_arr=[]
    rows = int(height / task_1a.CELL_SIZE)
    cols = int(width / task_1a.CELL_SIZE)
    d1 = 0
    for y in range(20, 40 * (rows), 40):
        for x in range(20, 40 * (cols), 40):
            t = 0
            for i in range(x - 16, x + 16, 1):
                t += img[i][y]
            if (t != 8160):
                coordinate_of_num.append((x, y))
                d1 = d1 + 1
    temp = np.zeros([16, 16], dtype=int)
    # print(coordinate_of_num)
    for y in range(0, d1):
        temp = img[(coordinate_of_num[y][0] - 16):(coordinate_of_num[y][0] + 16), (coordinate_of_num[y][1] - 16):(coordinate_of_num[y][1] + 16)]
        temp = cv2.resize(255 - temp, (28, 28))
        img_arr.append(temp)
    # str1='temp'+str(y)
    # cv2.imshow(str1,temp)
    return img_arr, coordinate_of_num


def digit_recog(image):
    global count
    # new_model = tf.keras.models.load_model("task1_c_n.model")

    temp = cv2.resize(255 - image, (26, 26))
    temp = np.pad(temp, ((1, 1), (1, 1)), "constant", constant_values=0)
    img_arr = temp.reshape(1, 28, 28, 1)
    img_arr = img_arr.astype('float32')
    img_arr /= 255
    #cv2.imshow("hehe",image)
    predictions = new_model.predict(img_arr)
    # pred = np.argmax(pred)
    #print(predictions.argmax())
    predictions = np.argmax(predictions)

    if (count == 0):
        import tensorflow as tf
        import keras
        # set number of categories
        num_category = 10
        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, num_category)
        y_test = keras.utils.to_categorical(y_test, num_category)
        # test = keras.utils.to_categorical(test , num_category)

        model = Sequential()
        # convolutional layer with rectified linear unit activation
        model.add(Conv2D(32, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=input_shape))
        # 32 convolution filters used each of size 3x3
        # again
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.30))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        # model.add(tf.keras.layers.Dropout(0.4))
        model.add(Dropout(0.35))
        model.add(Dense(num_category, activation='softmax'))
        model.compile(loss=keras.losses.categorical_crossentropy,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy'])
        batch_size = 128
        num_epoch = 30
        # model training
        model_log = model.fit(X_train, y_train,
                              batch_size=batch_size,
                              epochs=num_epoch,
                              verbose=1,
                              validation_data=(X_test, y_test))

        count = 1
        temp = cv2.resize(255 - image, (26, 26))
        temp = np.pad(temp, ((1, 1), (1, 1)), "constant", constant_values=0)
        img_arr = temp.reshape(1, 28, 28, 1)
        img_arr = img_arr.astype('float32')
        img_arr /= 255
        # cv2.imshow("hehe",image)
        predictions = new_model.predict(img_arr)
        # pred = np.argmax(pred)
        # print(predictions.argmax())
        predictions = np.argmax(predictions)


    else:
        temp = cv2.resize(255 - image, (26, 26))
        temp = np.pad(temp, ((1, 1), (1, 1)), "constant", constant_values=0)
        img_arr = temp.reshape(1, 28, 28, 1)
        img_arr = img_arr.astype('float32')
        img_arr /= 255
        # cv2.imshow("hehe",image)
        predictions = new_model.predict(img_arr)
        # pred = np.argmax(pred)
        # print(predictions.argmax())
        predictions = np.argmax(predictions)

    return predictions


#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling computeSum
# 					function, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1c_images' folder or not

if __name__ != '__main__':

    curr_dir_path = os.getcwd()

    # Importing task_1a and image_enhancer script
    try:

        task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
        sys.path.append(task_1a_dir_path)

        import task_1a
        import image_enhancer

    except Exception as e:

        print('\ntask_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
        exit()

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    img_dir_path = curr_dir_path + '/../task_1c_images/'				# path to directory of 'task_1c_images'

    file_num = 0
    img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

    # Importing task_1a and image_enhancer script
    try:

        task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
        sys.path.append(task_1a_dir_path)

        import task_1a
        import image_enhancer

    except Exception as e:

        print('\n[ERROR] task_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
        exit()

    # modify the task_1a.CELL_SIZE to 40 since maze images
    # in task_1c_images folder have cell size of 40 pixels
    task_1a.CELL_SIZE = 40

    print('\n============================================')

    print('\nFor maze0' + str(file_num) + '.jpg')

    try:
        original_binary_img = task_1a.readImage(img_file_path)
        height, width = original_binary_img.shape

    except AttributeError as attr_error:

        print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
        exit()


    no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
    no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
    initial_point = (0, 0)											# start point coordinates of maze
    final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

    try:

        shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)
        #print(shortestPath)

        if len(shortestPath) > 2:

            img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)

        else:

            print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
            exit()

    except TypeError as type_err:

        print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
        exit()

    print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

    digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

    print('\nDigits in the image = ', digits_list)
    print('\nDigits on shortest path in the image = ', digits_on_path)
    print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

    print('\n============================================')

    cv2.imshow('canvas0' + str(file_num), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = len(os.listdir(img_dir_path))

        for file_num in range(file_count):

            img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

            print('\n============================================')

            print('\nFor maze0' + str(file_num) + '.jpg')

            try:

                original_binary_img = task_1a.readImage(img_file_path)
                height, width = original_binary_img.shape

            except AttributeError as attr_error:

                print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
                exit()


            no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
            no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
            initial_point = (0, 0)											# start point coordinates of maze
            final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

            try:

                shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

                if len(shortestPath) > 2:

                    img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)

                else:

                    print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
                    exit()

            except TypeError as type_err:

                print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
                exit()

            print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

            digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

            print('\nDigits in the image = ', digits_list)
            print('\nDigits on shortest path in the image = ', digits_on_path)
            print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

            print('\n============================================')

            cv2.imshow('canvas0' + str(file_num), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    else:

        print('')



