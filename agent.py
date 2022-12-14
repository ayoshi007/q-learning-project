#####################################################################################################################
#
# This code is for the Final Project of UTD F22 CS 4375.001 Introduction to Machine Learning course.
# Created by Akihiro "Aki" Yoshimoto and Garyn Varela-Moody
#
#####################################################################################################################
import numpy as np
import random
import math
from constants import *
import sys

class Agent:
	def __init__(self, maze, show_gui: bool, starting_row=0, starting_col=0):
		self.maze = maze
		self.start_pos = (starting_row, starting_col)
		self.cur_pos = (starting_row, starting_col)
		self.q_table = np.zeros((maze.board.nrows, maze.board.ncols, 4))
		self.cur_epsilon = None #EPISLON WAS RENAMED TO CUR EPSILON FOR EASY CHANGE BETWEEN DECAY AND NON DECAY
		self.gamma = None
		self.learning_rate = None
		self.max_iter = None
		self.show_gui = show_gui
		
		self.episode_steps = []
		self.episode_rewards = []
	
	
	def set_hyperparameters(self, learning_rate, epsilon, epsilon_end, gamma, max_iter,epsilon_decay:bool,lr_decay:bool,random_training:bool):
		self.learning_rate = learning_rate
		self.epsilon_init = epsilon
		self.cur_epsilon = epsilon
		self.epsilon_end = epsilon_end
		self.gamma = gamma
		self.max_iter = max_iter
		self.ep_decay = epsilon_decay
		self.lr_decay = lr_decay
		self.random_training = random_training

		if self.lr_decay:
			self.learning_rate = 1

	def epsilon_decay(self,i):
		self.cur_epsilon = (self.epsilon_init - self.epsilon_end) * ((self.max_iter - 1 - i) / (self.max_iter - 1)) + self.epsilon_end

	def learning_rate_decay(self,i):
		self.learning_rate = self.max_iter/(self.max_iter + i)

	#RESETS QTABLE
	def reset_table(self): 
		self.q_table = np.zeros((self.maze.board.nrows, self.maze.board.ncols, 4))
		self.episode_steps = []
		self.episode_rewards = []

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

	def q_train(self,random_locations):
		self.limit = math.inf
		# perform max_iter episodes
		for i in range(self.max_iter):
			if self.ep_decay:
				self.epsilon_decay(i)
			if self.lr_decay:
				self.learning_rate_decay(i)
				
			if self.random_training:
				self.move(self.cur_pos, random.choice(random_locations))
			

			if self.show_gui:
				self.maze.update_board_title(f'({self.maze.run_number}/{self.maze.total_runs}) LR: {self.learning_rate:.2f}, Eps: {self.cur_epsilon:.2f}, Gamma: {self.gamma}, max_it: {self.max_iter}, Episode {i}')
			elif self.show_gui is not None:
				print(f'LR: {self.learning_rate:.2f}, Eps: {self.cur_epsilon:.2f}, Gamma: {self.gamma}, max_it: {self.max_iter}, Episode {i}  Steps: ', end='')
				sys.stdout.flush()
			self.maze.reset_goals()
			steps,rewards,cr = self.run_episode()
			
			if self.show_gui is not None and not self.show_gui:
				print(steps)
				sys.stdout.flush()
			
			self.episode_steps.append(steps)
			self.episode_rewards.append(rewards)
			self.reset_position()
			
	
	def q_test(self, test_number, test_location, limit) -> int:
		self.cur_epsilon = 0
		self.move(self.cur_pos, test_location)
		self.limit = limit
		lr_init = 1 if self.lr_decay else self.learning_rate
		
		if self.show_gui:
			self.maze.update_board_title(f'({self.maze.run_number}/{self.maze.total_runs}) LR_init: {lr_init:.2f}, Eps_init: {self.epsilon_init:.2f}, Gamma: {self.gamma}, max_it: {self.max_iter}, Final test {test_number}')
		elif self.show_gui is not None:
			print(f'LR_init: {lr_init:.2f}, Eps_init: {self.epsilon_init:.2f}, Gamma: {self.gamma}, max_it: {self.max_iter}, Final test {test_number} starting from ({test_location[0]}, {test_location[1]}): ', end='')
			sys.stdout.flush()
		
		pretest_q_table = self.q_table
		steps, rewards, cr = self.run_episode()
		self.q_table = pretest_q_table
		
		if self.show_gui:
			self.maze.update_board_title(f'({self.maze.run_number}/{self.maze.total_runs}) Final test {test_number}, start_loc ({test_location[0]}, {test_location[1]}): {"Goal found" if cr else "No goal"}, steps {steps}, reward {rewards}')
		elif self.show_gui is not None:
			print(f' Goal found: {cr}, steps {steps}, reward {rewards}')
			sys.stdout.flush()
			
		return steps, rewards, cr
	

	
	def run_episode(self):
		done = False
		steps = 0
		reward = 0
		cr = False
		# perform episode
		while not done and not(steps > self.limit):
			old_pos = self.cur_pos
			surroundings = self.maze.get_surroundings(old_pos[0], old_pos[1])
			
			# explore
			if random.uniform(0, 1) < self.cur_epsilon:
				action = random.randint(0, 3)
			# exploit
			else:
				action = np.argmax(self.q_table[self.cur_pos[0]][self.cur_pos[1]])
			
			#print(self.q_table)
			valid = False if surroundings[action] == 'w' else True
			
			immediate_reward = self.maze.get_reward(old_pos[0], old_pos[1], action)
			reward += immediate_reward
			new_pos = self.get_new_pos(old_pos, action, valid)
			
			self.table_update(old_pos, action, immediate_reward, new_pos)
			
			done = self.move(old_pos, new_pos)
			steps += 1
		if done:
			cr = True
		return steps, reward, cr

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
