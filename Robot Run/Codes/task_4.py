
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 4 of Rapid Rescuer (RR) Theme (eYRC 2019-20).
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


# Team ID:			[ For e.g., 9999 ]
# Author List:		[ Comma separated list of author names ]
# Filename:			task_4.py
# Functions:		connect_to_server, send_to_receive_from_server, find_new_path, create_combination_dict,
# 					python_client, take_input_for_reposition_restart, service_shutdown
# 					[ Comma separated list of functions in this file ]
# Global variables:	SERVER_IP, SERVER_PORT, SERVER_ADDRESS, sock
# 					[ List of global variables defined in this file ]


# Import necessary modules
# Do not import any other modules
import cv2
import socket
import sys
import os
from collections import defaultdict, Counter
import signal, threading

new_intial_point=(0,0)
# IP address of robot-server (ESP32)
SERVER_IP = '192.168.4.1'

# Port number assigned to server
SERVER_PORT = 3333
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

# global 'sock' variable for socket connection
sock = None


def connect_to_server(SERVER_ADDRESS):

	"""
	Purpose:
	---
	the function creates socket connection with server

	Input Arguments:
	---
	`SERVER_ADDRESS` :	[ tuple ]
		port address of server

	Returns:
	---
	`sock` :	[ object of socket class ]
		object of socket class for socket communication

	Example call:
	---
	sock = connect_to_server(SERVER_ADDRESS)

	"""

	global sock
	sock = None

	#############  Add your Code here   ###############
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(SERVER_ADDRESS)


	###################################################

	return sock


def send_to_receive_from_server(sock, data_to_send):

	"""
	Purpose:
	---
	the function sends / receives data to / from server in proper format

	Input Arguments:
	---
	`sock` :	[ object of socket class ]
		object of socket class for socket communication
	`string`	:	[ string ]
		data to be sent from client to server

	Returns:
	---
	`sent_data` :	[ string ]
		data sent from client to server in proper format
	`recv_data` :	[ string ]
		data sent from server to client in proper format

	Example call:
	---
	sent_data, recv_data = send_to_receive_from_server(sock, shortestPath)

	"""

	sent_data = ''
	recv_data = ''

	#############  Add your Code here   ###############
	sent_data = '#' + str(data_to_send) + '#'
	sock.sendall(sent_data.encode())

	recv_data = sock.recv(1024)  # earlier 128
	# print(recv_data)
	recv_data = recv_data.decode()
	#print(recv_data)


	# Look for the response
	# amount_received = 0
	#print("recv data= ",recv_data1)
	# amount_received += len(recv_data)


	###################################################

	return sent_data, recv_data


def find_new_path(recv_data, shortestPath):

	"""
	Purpose:
	---
	the function computes new shortest path from cell adjacent to obstacle to final_point

	Input Arguments:
	---
	`recv_data` :	[ string ]
		data sent from server to client in proper format
	`shortestPath`	:	[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Returns:
	---
	`obstacle_coord` :	[ tuple ]
		position of dynamic obstacle in (x,y) coordinate
	`new_shortestPath` :	[ list ]
		list of coordinates of shortest path from new_initial_point to final_point
	`new_initial_point` :	[ tuple ]
		coordinate of cell adjacent to obstacle for the new shortest path
	`img` :	[ numpy array ]

	Example call:
	---
	obstacle_coord, new_shortestPath, new_initial_point, img = find_new_path(recv_data, shortestPath)

	"""

	obstacle_coord = ()
	new_shortestPath = []
	new_initial_point = ()

	global img_file_path, final_point, no_cells_height, no_cells_width

	#############  Add your Code here   ###############
	open_brack_idx = recv_data.find('(')
	comma_idx = recv_data.find(',')
	close_brack_idx = recv_data.find(')')

	if abs((open_brack_idx - comma_idx)) > 2:
		obstacle_x = (int(recv_data[comma_idx-2]))*10 + (int(recv_data[comma_idx-1]))
	else:
		obstacle_x = (int(recv_data[comma_idx-1]))

	if abs((close_brack_idx - comma_idx)) > 2:
		obstacle_y = (int(recv_data[comma_idx+1]))*10 + (int(recv_data[comma_idx+2]))
	else:
		obstacle_y = (int(recv_data[comma_idx+1]))

	obstacle_coord = (obstacle_x, obstacle_y)

	obstacle_list.append(obstacle_x)
	obstacle_list.append(obstacle_y)

	# colour the cell as blocked at the obstacle's position
	obstacle_index = shortestPath.index((obstacle_x, obstacle_y))
	new_final_point = shortestPath[obstacle_index-1] # (0, 0)                  # start coordinates of maze
	img = task_1a.readImage(img_file_path)

	obstacle_pos = 0

	while obstacle_pos < len(obstacle_list):
		# print(obstacle_pos, len(obstacle_list), obstacle_list[obstacle_pos], obstacle_list[obstacle_pos+1])
		image_enhancer.colourCell(img, obstacle_list[obstacle_pos], obstacle_list[obstacle_pos+1], 0)
		obstacle_pos = obstacle_pos + 2
		# cv2.imshow('colored' + str(obstacle_pos), img)

	new_shortestPath = task_1a.solveMaze(img, new_initial_point, new_final_point, no_cells_height, no_cells_width)
	new_initial_point=new_final_point

	###################################################

	return obstacle_coord, new_shortestPath, new_initial_point, img


#############	You can add other helper functions here		#############
def send_data(sock,data):
	sent_data = '#' + str(data) + '#' + '\x00'
	sock.sendall(sent_data.encode())
	return sent_data
def recv_data(sock):
	recv_data = sock.recv(1024)  # earlier 128
	recv_data = recv_data.decode()
	return recv_data

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def create_combination_dict(combination_digits, combination_locations):

	"""
	Purpose:
	---
	the function takes digits and locations and returns appropriate dictionary for combination chosen,
	it handles the existence of two duplicate keys (digits) in a dictionary

	Input Arguments:
	---
	`combination_digits` :	[ list of integers ]
		list of digits chosen in the combination of Sum
	`combination_locations`	:	[ list of tuples ]
		list of locations in maze image of digits chosen in the combination of Sum

	Returns:
	---
	`combination` :	[ dict ]
		appropriate dictionary for the combination of digits chosen for the Sum,
		it handles the existence of two duplicate keys (digits) in a dictionary

	Example call:
	---
	combination = create_combination_dict(combination_digits, combination_locations)

	"""

	combination = defaultdict(list)
	loc = 0

	combination_digits_count = Counter(combination_digits)

	for digit in combination_digits:
		if combination_digits_count[digit] > 1:
			combination[digit].append(combination_locations[loc])
		else:
			combination[digit] = combination_locations[loc]
		loc = loc + 1

	combination.default_factory = None
	combination = dict(combination)

	return combination


# NOTE:	YOU ARE ALLOWED TO MAKE CHANGE TO THIS FUNCTION ONLY WHERE SPECIFIED BELOW
def python_client():

	try:

		curr_dir_path = os.getcwd()
		img_dir_path = curr_dir_path + '/../Maze_Image/'		# path to directory of 'Maze_Image'

		img_file_path = img_dir_path + '/Task4_maze.jpg'		# path to 'Task4_maze.jpg' image file

		# Importing task_1a and image_enhancer script
		try:

			task_1a_dir_path = curr_dir_path
			sys.path.append(task_1a_dir_path)

			import task_1a
			import image_enhancer

			# changing the 'CELL_SIZE' variable to 40 x 40 pixels in accordance with the size in image
			task_1a.CELL_SIZE = 40

		except Exception as e:
			print('\n[ERROR] task_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
			exit()

		# Read the image and find the shortest path
		try:
			original_binary_img = task_1a.readImage(img_file_path)
			height, width = original_binary_img.shape

		except AttributeError as attr_err:
			print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
			exit()

		no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
		no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image

		try:

			print('\n============================================')

			# Create socket connection with server
			try:
				sock = connect_to_server(SERVER_ADDRESS)

				if sock == None:
					print('\n[ERROR] connect_to_server function is not returning socket object in expected format !\n')
					exit()

				else:
					print('\nConnecting to %s Port %s' %(SERVER_ADDRESS))

			except ConnectionRefusedError as connect_err:
				print('\n[ERROR] the robot-server.c file is not executing, start the server first !\n')
				exit()

			# Send the 'digits_list' and 'combination_of_digits' to robot
			digits_list = [8, 0, 2, 2]

			combination_digits = [2, 2]
			combination_locations = [(6,9), (8,6)]

			combination = create_combination_dict(combination_digits, combination_locations)

			print('\nGiven Digits in image = %s \n\nGiven Combination of Digits with Locations = %s' % (digits_list, combination))
		except Exception:
			pass

			#############  NOTE: Edit this part to complete the Task 4 implementation   ###############
		sent = ''
		received = ''
		length = 0
		for x in combination:
			temp1 = len(combination[x])
			length = length + temp1
		# sent_data_i = "hello"
		# sent, received = send_to_receive_from_server(sock, sent_data_i)
		# while received[1] != 's':
		# 	sent, received = send_to_receive_from_server(sock,sent_data_i)
		sent_data_f = str(digits_list) + '|' +str(combination)
		# send_data(sock,sent_data_f)
		# initial_point1 = (4, 4)  # start point coordinates of maze
		# final_point1 = ((no_cells_height - 1), (no_cells_width - 1))
		# shortestPath1 = solveMaze(original_binary_img, initial_point1, final_point1, no_cells_height, no_cells_width)
		initial_point1 = (4, 4)
		new_path1= [[]]
		v=0
		for x in combination_locations:
			final_point1 = x
			np=(task_1a.solveMaze(original_binary_img, initial_point1, final_point1, no_cells_height,no_cells_width))
			new_path1.append(np)
			v=v+1
			# send_data(sock,new_path)
			initial_point1=final_point1
		new_path="|"
		for x in new_path1:
			new_path=new_path+str(x)+"|"
		# send_data(sock,new_path)
		for i in range(0,4):
			send_data(sock,"okay")
			received = recv_data(sock)
			print("%s"%received)
		# while received[1] != '$':
		# 	received = recv_data(sock)
		# received=recv_data(sock)
		# while received[1]!='H':
		# 		received=recv_data(sock)
			##########################################################################################

	except KeyboardInterrupt:

		sys.exit()


# NOTE:	YOU ARE ALLOWED TO EDIT THIS FUNCTION
def take_input_for_reposition_restart():

	global sock

	try:

		while True:

			data_to_send = input('\nEnter either "%" for Restart OR "&" for Reposition: \n')

			if (data_to_send == '%') or (data_to_send == '&'):

				if (data_to_send == '%'):

					print('\nOne Restart for the run is taken !')

					sent_data = str(data_to_send)
					sock.sendall(sent_data.encode())

					print('\nClosing Socket')

					sock.close()

					sys.exit()

				elif (data_to_send == '&'):

					print('\nOne Reposition for the run is taken !')

					sent_data = str(data_to_send)
					sock.sendall(sent_data.encode())

					#############  NOTE: Edit this part to complete the Task 4 implementation   ###############



					##########################################################################################

			else:

				print('\nYou must enter either "%" OR "&" only !')

	except KeyboardInterrupt:

		print('\nClosing Socket')
		sock.close()

		sys.exit()


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS CLASS
class ServiceExit(Exception):
	"""
	Custom exception which is used to trigger the clean exit
	of all running threads and the main program.
	"""
	pass


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def service_shutdown(signum, frame):
	print('Caught signal %d' % signum)
	raise ServiceExit


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function creates two independent Threads, one for running the Python Client program,
# 					second to take the user input for Restart ( " % " ) or Reposition ( " & " ) as per the Rulebook

if __name__ == '__main__':

	try:

		# Register the signal handlers
		signal.signal(signal.SIGTERM, service_shutdown)
		signal.signal(signal.SIGINT, service_shutdown)

		# creating thread
		t1 = threading.Thread(target=python_client, name='python_client')
		t2 = threading.Thread(target=take_input_for_reposition_restart, name='take_input_for_reposition_restart')

		t1.shutdown_flag = threading.Event()
		t2.shutdown_flag = threading.Event()

		# starting thread 1
		t1.start()
		# starting thread 2
		t2.start()

	except ServiceExit:

		t1.shutdown_flag.set()
		t2.shutdown_flag.set()

		# wait until thread 1 is completely executed
		t1.join(1)
		# wait until thread 2 is completely executed
		t2.join(1)

		# both threads completely executed
		print("Done!")

