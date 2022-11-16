from game2dboard import Board
import numpy as np
from constants import *
class Agent:
	def __init__(self, starting_row=0, starting_col=0):
		self.row = starting_row
		self.col = starting_col
		self.position  = (starting_row,starting_col)

	#GETS NUMBER OF STATES 
	def getting_number_of_states(self,board:Board):
		self.num_states = board.size **4
		self.table_init()
	
	#GETS CURRENT STATE IN REFERENCE TO AGENT AND GOAL POSITION
	def get_state(self,board:Board,goal:tuple):
		state = self.position[0] * board.size**3
		state = state + self.position[1] * board.size**2
		state = state + goal[0] * board.size
		state = state + goal[1]
		return state

	#INITIATES QTABLE
	def table_init(self):
		num_states = self.num_states
		num_actions = 4
		#self.q_table = np.zeros((num_states,num_actions),dtype='uint8')
		self.q_table = np.zeros((num_states,num_actions))

	#RETURNS QTABLE
	def get_qtable(self):
		return self.q_table

	#Q[STATE,ACTION] = Q[STATE,ACTION] + LEARNING_RATE * (REWARD + GAMMA * MAX(Q[NEW STATE])-Q[STATE,ACTION])
	#GAMMA: IS DISCOUNT FACTOR, TYPICALLY (.8 TO .99)
	#UPDATES QTABLE
	def table_update(self,state,action,reward,new_state): 
		self.q_table[state,action] = self.q_table[state,action] + LEARNING_RATE * (reward + GAMMA * np.max(self.q_table[new_state])-self.q_table[state,action])

	#RESETS POSITION OF AGENT AFTER ONE RUN
	def reset_position(self):
		self.position = (self.row,self.col)

	#FUNCTION FOR MOVING AGENT
	def move(self,board:Board,action):
		(x,y) = self.position
		if action == 0: #Go Up
			if board[x][y-1] == 'wall_resize.png':
				return -10, False
			elif board[x][y-1] == 'goal_resize.png':
				return 20, True
			else:
				self.position = (x,y-1)
				return -1, False
		elif action == 1: #Go Down
			if board[x][y+1] == 'wall_resize.png':
				return -10, False
			elif board[x][y+1] == 'goal_resize.png':
				return 20, True
			else:
				self.position = (x,y+1)
				return -1, False
		elif action == 2: #Go Right
			if board[x+1][y] == 'wall_resize.png':
				return -10, False
			elif board[x+1][y] == 'goal_resize.png':
				return 20, True
			else:
				self.position = (x+1,y)
				return -1, False
		elif action == 3: #Go Left
			if board[x-1][y] == 'wall_resize.png':
				return -10, False
			elif board[x-1][y] == 'goal_resize.png':
				return 20, True
			else:
				self.position = (x-1,y)
				return -1, False
		

	# def move_up():
	# 	self.row -= 1
	# def move_down():
	# 	self.row += 1
	# def move_right():
	# 	self.col += 1
	# def move_left():
	# 	self.col -= 1