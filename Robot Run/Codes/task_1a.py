
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1A of Rapid Rescuer (RR) Theme (eYRC 2019-20).
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
# Filename:			task_1a.py
# Functions:		readImage, solveMaze
# 					[ Comma separated list of functions in this file ]
# Global variables:	CELL_SIZE
# 					[ List of global variables defined in this file ]


# Import necessary modules
# Do not import any other modules
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Task4_maze.jpg have cell size of 40 pixels
CELL_SIZE = 40


def readImage(img_file_path):

    """
    Purpose:
    ---
    the function takes file path of original image as argument and returns it's binary form

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `original_binary_img` :	[ numpy array ]
        binary form of the original image at img_file_path

    Example call:
    ---
    original_binary_img = readImage(img_file_path)

    """

    binary_img = None

    #############	Add your Code here	###############
    img1 = cv2.imread(img_file_path)
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    # cv2.imshow("b", binary_img)
    # np.set_printoptions(threshold=np.inf)
    # print(binary_img)
    # cv2.waitKey(0)
    ###################################################

    return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

    """
    Purpose:
    ---
    the function takes binary form of original image, start and end point coordinates and solves the maze
    to return the list of coordinates of shortest path from initial_point to final_point

    Input Arguments:
    ---
    `original_binary_img` :	[ numpy array ]
        binary form of the original image at img_file_path
    `initial_point` :		[ tuple ]
        start point coordinates
    `final_point` :			[ tuple ]
        end point coordinates
    `no_cells_height` :		[ int ]
        number of cells in height of maze image
    `no_cells_width` :		[ int ]
        number of cells in width of maze image

    Returns:
    ---
    `shortestPath` :		[ list ]
        list of coordinates of shortest path from initial_point to final_point

    Example call:
    ---
    shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

    """
    
    shortestPath = []

    #############	Add your Code here	###############
    h = no_cells_height * CELL_SIZE
    w = no_cells_width * CELL_SIZE
    h_ = no_cells_height
    w_ = no_cells_width
    grid= Maze_matrix(original_binary_img, no_cells_height, no_cells_width)
    maze = grid
    start = [2 * initial_point[0] + 1, 2 * initial_point[1] + 1]
    end = [2 * final_point[0] + 1, 2 * final_point[1] + 1]
    cost = 1
    path = search(maze, cost, start, end)
    short1 = []
    short2 = []
    short = []
    # print(np.array(path).shape)
    # print(2 * final_point[0] + 1)
    # print(2 * final_point[1] + 1)
    # print(path[2 * final_point[0] + 1][2 * final_point[1] + 1] +1)
    # print(np.array(path))
    for i in range(path[2 * final_point[0] + 1][2 * final_point[1] + 1] + 1):
        for j in range(2 * final_point[0] + 2):
            for k in range(2 * final_point[1] + 2):
                if i == path[j][k]:
                    short1.append((j, k))
    # print(short1)
    for i in range(len(short1)):
        if i % 2 == 0:
            short2.append(short1[i])
    for i in range(len(short2)):
        short.append((int((short2[i][0] - 1) / 2), int((short2[i][1] - 1) / 2)))
    for i in range(len(short)):
        shortestPath.append(short[i])
    # print(shortestPath)
    ###################################################
    
    return shortestPath


#############	You can add other helper functions here		#############
def Maze_matrix(maze1, no_cells_height1, no_cells_width1):
    matrix = np.zeros((2 * (no_cells_height1) - 1, 2 * (no_cells_width1) - 1), dtype=int)
    for i in range(1, 2 * (no_cells_width1 - 1), 2):
        for j in range(1, 2 * (no_cells_height1 - 1), 2):
            matrix[i][j] = 1

    for i in range(0, (no_cells_width1)):
        for j in range(0, (no_cells_height1 - 1)):
                if maze1[CELL_SIZE * (i) + int(CELL_SIZE/2)][CELL_SIZE*(j+1)] == 0:
                    matrix[2 * i][(2 * j) + 1] = 1


    for i in range(0, (no_cells_width1 - 1)):
        for j in range(0, (no_cells_height1)):
                if maze1[CELL_SIZE*(i+1)][CELL_SIZE * (j) + int(CELL_SIZE/2)] == 0:
                    matrix[(2 * i) + 1][2 * j] = 1

    np.set_printoptions(threshold=np.inf)
    #print(matrix)
    ls = matrix.tolist()
    lsb = matrix.tolist()
    ln= np.ones((1,2*(no_cells_width1)-1),dtype=int).tolist()
    lsb = lsb + ln
    lsb = ln + lsb
    for i in range(0,2*no_cells_height1):
        lsb[i].append(1)
        lsb[i].insert(0, 1)
    matrix1=np.asarray(lsb)
    #print(matrix1)
    return matrix1
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

def return_path(curr,maze):
    pathe = []
    row, col = np.shape(maze)
    res = [[-1 for i in range(col)] for j in range(row)]
    current = curr
    while current is not None:
        pathe.append(current.position)
        current = current.parent
    pathe = pathe[::-1]
    start = 0
    for i in range(len(pathe)):
        res[pathe[i][0]][pathe[i][1]] = start
        start += 1
    return res


def search(maze, costs, start, end):
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0
    visit_list = []
    visited_list = []
    visit_list.append(start_node)
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10
    move  =  [[-1, 0 ],
          [ 0, -1],
          [ 1, 0 ],
          [ 0, 1 ]]
    no_rows, no_columns = np.shape(maze)
    while len(visit_list) > 0:
        outer_iterations += 1
        current_node = visit_list[0]
        current_index = 0
        for index, item in enumerate(visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        if outer_iterations > max_iterations:
            print ("givin' up o..o..")
            return return_path(current_node,maze)
        visit_list.pop(current_index)
        visited_list.append(current_node)
        if current_node == end_node:
            return return_path(current_node,maze)
        childrun = []
        for new_pos in move:
            node_pos = (current_node.position[0] + new_pos[0], current_node.position[1] + new_pos[1])
            if (node_pos[0] > (no_rows - 1) or node_pos[0] < 0 or node_pos[1] > (no_columns -1) or node_pos[1] < 0):
                continue
            if maze[node_pos[0]][node_pos[1]] != 0:
                continue
            new_node = Node(current_node, node_pos)
            childrun.append(new_node)
        for child in childrun:
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue
            child.g = current_node.g + costs
            child.h = (((child.position[0] - end_node.position[0])) + ((child.position[1] - end_node.position[1])))
            child.f = child.g + child.h
            if len([i for i in visit_list if child == i and child.g > i.g]) > 0:
                continue
            visit_list.append(child)


#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    img_dir_path = curr_dir_path + '/../Maze_Image/'        # path to directory of 'Maze_Image'

    file_num = 0
    img_file_path = img_dir_path + '/Task4_maze.jpg'        # path to 'Task4_maze.jpg' image file

    print('\n============================================')

    print('\nFor Task4_maze.jpg')

    try:
        
        original_binary_img = readImage(img_file_path)
        height, width = original_binary_img.shape

    except AttributeError as attr_error:
        
        print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
        exit()
    
    no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
    no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
    initial_point = (0, 0)											# start point coordinates of maze
    final_point = (9,9)			# end point coordinates of maze

    try:

        shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

        if len(shortestPath) > 2:

            img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
            
        else:

            print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
            exit()
    
    except TypeError as type_err:
        
        print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
        exit()

    print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
    
    print('\n============================================')
    
    cv2.imshow('canvas0' + str(file_num), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


