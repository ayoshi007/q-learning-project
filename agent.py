from game2dboard import Board
import numpy as np
import random
from constants import *

class Agent:
	def __init__(self, maze, show_gui, starting_row=0, starting_col=0):
		self.maze = maze
		self.start_pos = (starting_row, starting_col)
		self.cur_pos = (starting_row, starting_col)
		self.q_table = np.zeros((maze.board.nrows, maze.board.ncols, 4))
		self.epsilon = None
		self.gamma = None
		self.learning_rate = None
		self.max_iter = None
		self.show_gui = show_gui
		
		self.episode_steps = []
	
	def get_history():
		return self.episode_steps
	
	def set_hyperparameters(self, learning_rate, epsilon, gamma, max_iter):
		self.learning_rate = learning_rate
		self.epsilon = epsilon
		self.gamma = gamma
		self.max_iter = max_iter

	#RESETS QTABLE
	def reset_table(self): 
		self.q_table = np.zeros((self.maze.board.nrows, self.maze.board.ncols, 4))

	#RETURNS QTABLE
	def get_qtable(self):
		return self.q_table
		
	#RESETS POSITION OF AGENT AFTER ONE RUN
	def reset_position(self):
		self.cur_pos = self.start_pos

	#Q[STATE,ACTION] = Q[STATE,ACTION] + LEARNING_RATE * (REWARD + GAMMA * MAX(Q[NEW STATE])-Q[STATE,ACTION])
	#GAMMA: IS DISCOUNT FACTOR, TYPICALLY (.8 TO .99)
	#UPDATES QTABLE
	def table_update(self, old_pos: tuple, action: int, reward, new_pos: tuple):
		delta = self.learning_rate * (reward + (self.gamma * np.max(self.q_table[new_pos[0]][new_pos[1]])) - self.q_table[old_pos[0]][old_pos[1]][action])
		self.q_table[old_pos[0]][old_pos[1]][action] += delta

	def q_train(self):
		# perform max_iter episodes
		for i in range(self.max_iter):
			if self.show_gui:
				self.update_board_title(f'LR: {self.learning_rate}, Eps: {self.epsilon}, Gamma: {self.gamma}, max_it: {self.max_iter}, Episode {i}')
			else:
				print(f'LR: {self.learning_rate}, Eps: {self.epsilon}, Gamma: {self.gamma}, max_it: {self.max_iter}, Episode {i}  Steps: ', end='')
			
			steps = self.run_episode()
			
			if not self.show_gui:
				print(steps)
			
			self.episode_steps.append(steps)
			self.reset_position()
			
	
	def q_test(self) -> int:
		if self.show_gui:
			self.update_board_title(f'LR: {self.learning_rate}, Eps: {self.epsilon}, Gamma: {self.gamma}, max_it: {self.max_iter}, Final test')
		else:
			print(f'LR: {self.learning_rate}, Eps: {self.epsilon}, Gamma: {self.gamma}, max_it: {self.max_iter}, Final test  Steps: ', end='')
		
		self.epsilon = 0
		steps = self.run_episode()
		
		if self.show_gui:
			self.update_board_title(f"Final test steps: {steps}")
		else:
			print(steps)
			print()
			
		return steps
	
	def update_board_title(self, new_title: str):
		self.maze.board.title = new_title
		self.maze.reset_goal()
		self.maze.board._root.update()
	
	def run_episode(self):
		done = False
		steps = 0
		# perform episode
		while not done:
			old_pos = self.cur_pos
			surroundings = self.maze.get_surroundings(old_pos[0], old_pos[1])
			
			actions = []
			# explore
			if random.uniform(0, 1) < self.epsilon:
				action = random.randint(0, 3)
			# exploit
			else:
				action = np.argmax(self.q_table[self.cur_pos[0]][self.cur_pos[1]])
			
			#print(self.q_table)
			valid = True
			if surroundings[action] == 'w':
				valid = False
			
			immediate_reward = self.maze.get_reward(old_pos[0], old_pos[1], action)
			new_pos = self.get_new_pos(old_pos, action, valid)
			
			self.table_update(old_pos, action, immediate_reward, new_pos)
			
			done = self.move(old_pos, new_pos)
			steps += 1
		return steps

	def get_new_pos(self, old_pos: tuple, action: int, valid: bool) -> tuple:
		if not valid:
			return old_pos
		
		if action == NORTH:
			return (old_pos[0] - 1, old_pos[1])
		elif action == EAST:
			return (old_pos[0], old_pos[1] + 1)
		elif action == SOUTH:
			return (old_pos[0] + 1, old_pos[1])
		return (old_pos[0], old_pos[1] - 1)
	
	#FUNCTION FOR MOVING AGENT
	def move(self, old_pos: tuple, new_pos: tuple) -> bool:
		if self.show_gui:
			self.maze.update_agent_gui(old_pos, new_pos)
		self.cur_pos = new_pos
		return self.maze.is_goal(new_pos[0], new_pos[1])