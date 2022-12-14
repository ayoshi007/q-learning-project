#####################################################################################################################
#
# This code is for the Final Project of UTD F22 CS 4375.001 Introduction to Machine Learning course.
# Created by Akihiro "Aki" Yoshimoto and Garyn Varela-Moody
#
#####################################################################################################################

from game2dboard import Board
from agent import Agent
import numpy as np
from recording import record_metrics, record_modelhistory, record_rewardhistory
from constants import *
import time
import sys

class Maze:
	def __init__(self, maze_name: str, board: Board, agent: tuple, goals: set, random_spots, testing_spots, show_gui=True):
		self.maze_name = maze_name
		self.board = board
		self.agent = Agent(self, show_gui, agent[0], agent[1])
		self.goals = goals
		
		self.random_spots = random_spots
		self.testing_spots = testing_spots	
		self.show_gui = show_gui
		
		# rewards is the reward given to the agent in each state, per its 4 possible actions
		self.rewards = np.ndarray((board.nrows, board.ncols, 4))
		self.init_rewards()
	
	# initialize the immediate rewards 2d array
	def init_rewards(self):
		for i in range(self.board.nrows):
			for j in range(self.board.ncols):
				self.rewards[i][j] = [FREE_MOVEMENT_PENALTY] * 4
				
				# the goal state is an absorbing state
				if self.board[i][j] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j] = [None] * 4
					
				# if adjacent state is non-existent or a wall, disallow movement
				# if adjacent state is the goal, then reward is 500
				# otherwise, i.e. adjacent state is an empty cell, reward is -1
				if i == 0:
					self.rewards[i][j][NORTH] = PUNISHMENT
				elif self.board[i - 1][j] == WALL_IMG_RESIZE_SRC:
					self.rewards[i][j][NORTH] = PUNISHMENT
				elif self.board[i - 1][j] == HAZARD_IMG_RESIZE_SRC:
					self.rewards[i][j][NORTH] = HAZARD_PUNISHMENT
				elif self.board[i - 1][j] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][NORTH] = REWARD
				
				if i == self.board.nrows - 1:
					self.rewards[i][j][SOUTH] = PUNISHMENT
				elif self.board[i + 1][j] == WALL_IMG_RESIZE_SRC:
					self.rewards[i][j][SOUTH] = PUNISHMENT
				elif self.board[i + 1][j] == HAZARD_IMG_RESIZE_SRC:
					self.rewards[i][j][SOUTH] = HAZARD_PUNISHMENT
				elif self.board[i + 1][j] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][SOUTH] = REWARD
				
				if j == 0:
					self.rewards[i][j][WEST] = PUNISHMENT
				elif self.board[i][j - 1] == WALL_IMG_RESIZE_SRC:
					self.rewards[i][j][WEST] = PUNISHMENT
				elif self.board[i][j - 1] == HAZARD_IMG_RESIZE_SRC:
					self.rewards[i][j][WEST] = HAZARD_PUNISHMENT
				elif self.board[i][j - 1] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][WEST] = REWARD
				
				if j == self.board.ncols - 1:
					self.rewards[i][j][EAST] = PUNISHMENT
				elif self.board[i][j + 1] == WALL_IMG_RESIZE_SRC:
					self.rewards[i][j][EAST] = PUNISHMENT
				elif self.board[i][j + 1] == HAZARD_IMG_RESIZE_SRC:
					self.rewards[i][j+1][EAST] = HAZARD_PUNISHMENT
				elif self.board[i][j + 1] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][EAST] = REWARD
	
	# update agent's position and the GUI
	def update_agent_gui(self, old_pos, new_pos):
		time.sleep(SLEEP)
		if old_pos == new_pos:
			return
		
		if old_pos in self.goals:
			self.board[old_pos[0]][old_pos[1]] = GOAL_IMG_RESIZE_SRC
		elif self.board[old_pos[0]][old_pos[1]] == AGENT_IN_HAZARD_IMG_RESIZE_SRC:
			self.board[old_pos[0]][old_pos[1]] = HAZARD_IMG_RESIZE_SRC
		else:
			self.board[old_pos[0]][old_pos[1]] = None
		
		
		if new_pos in self.goals:
			self.board[new_pos[0]][new_pos[1]] = AGENT_GOALIN_IMG_RESIZE_SRC
		elif self.board[new_pos[0]][new_pos[1]] == HAZARD_IMG_RESIZE_SRC:
			self.board[new_pos[0]][new_pos[1]] = AGENT_IN_HAZARD_IMG_RESIZE_SRC
		else:
			self.board[new_pos[0]][new_pos[1]] = AGENT_IMG_RESIZE_SRC
		
		self.board._root.update()
	
	def update_board_title(self, new_title: str):
		self.board.title = new_title
		self.board._root.update()
	
	# used by agent to get immediate surroundings, which are a part of the agent's state
	def get_surroundings(self, r, c) -> tuple:
		surroundings = ['f', 'f', 'f', 'f']
		
		if r == 0 or self.board[r - 1][c] == WALL_IMG_RESIZE_SRC:
			surroundings[NORTH] = 'w'
		elif self.board[r - 1][c] == HAZARD_IMG_RESIZE_SRC:
			surroundings[NORTH] = 'h'
		elif self.board[r - 1][c] == GOAL_IMG_RESIZE_SRC:
			surroundings[NORTH] = 'g'
			
		if r == self.board.nrows - 1 or self.board[r + 1][c] == WALL_IMG_RESIZE_SRC:
			surroundings[SOUTH] = 'w'
		elif self.board[r + 1][c] == HAZARD_IMG_RESIZE_SRC:
			surroundings[SOUTH] = 'h'
		elif self.board[r + 1][c] == GOAL_IMG_RESIZE_SRC:
			surroundings[SOUTH] = 'g'
			
		if c == 0 or self.board[r][c - 1] == WALL_IMG_RESIZE_SRC:
			surroundings[WEST] = 'w'
		elif self.board[r][c - 1] == HAZARD_IMG_RESIZE_SRC:
			surroundings[WEST] = 'h'
		elif self.board[r][c - 1] == GOAL_IMG_RESIZE_SRC:
			surroundings[WEST] = 'g'
			
		if c == self.board.ncols - 1 or self.board[r][c + 1] == WALL_IMG_RESIZE_SRC:
			surroundings[EAST] = 'w'
		elif self.board[r][c + 1] == HAZARD_IMG_RESIZE_SRC:
			surroundings[EAST] = 'h'
		elif self.board[r][c + 1] == GOAL_IMG_RESIZE_SRC:
			surroundings[EAST] = 'g'
		
		return tuple(surroundings)
	
	def get_reward(self, r, c, action):
		return self.rewards[r][c][action]
	
	def is_goal(self, r, c):
		return (r, c) in self.goals
	
	def reset_goals(self):
		for goal in self.goals:
			self.board[goal[0]][goal[1]] = GOAL_IMG_RESIZE_SRC
	
	def start(self, hyperparameters, repeats, total_runs):
		np.seterr('raise')
		self.hyperparameters = hyperparameters
		self.repeats = repeats
		self.total_runs = total_runs
		if self.show_gui:
			self.board.on_start = self.run_hyperparameters
			self.board.show()
		else:
			self.run_hyperparameters()
	
	def run_hyperparameters(self):
		test_steps = []
		test_reward = []
		test_cr = []
		self.run_number = 1
		print(f"Running {self.total_runs} hyperparameter combinations")
		sys.stdout.flush()
		for learning_rate, epsilon, epsilon_end, gamma, max_iter, epsilon_decay, lr_decay, random_training in self.hyperparameters:
			for _ in range(self.repeats):
				print(f'Run {self.run_number}/{self.total_runs}')
				sys.stdout.flush()
				self.agent.reset_position()
				self.agent.reset_table()
				
				self.agent.set_hyperparameters(learning_rate,epsilon, epsilon_end, gamma, max_iter, epsilon_decay, lr_decay, random_training)
				
				self.agent.q_train(self.random_spots)

				avrg_training_steps = sum(self.agent.episode_steps) / max_iter
				avrg_training_reward = sum(self.agent.episode_rewards) / max_iter
				
				hard_limit = int(avrg_training_steps * 2)

				print()
				for i, test_start in enumerate(self.testing_spots):
					self.reset_goals()
					s, r, cr = self.agent.q_test(i + 1, test_start, hard_limit)
					test_steps.append(s)
					test_reward.append(r)
					test_cr.append(cr)
					
					if self.show_gui:
						time.sleep(1)
				print()
				
				
				record_metrics(self.maze_name, random_training, learning_rate, lr_decay, epsilon, epsilon_end, epsilon_decay, gamma, max_iter, test_cr,test_steps,test_reward, avrg_training_steps, avrg_training_reward)
				record_modelhistory(self.agent.episode_steps)
				record_rewardhistory(self.agent.episode_rewards)
				
				test_steps = []
				test_reward = []
				test_cr = []
						
				self.run_number += 1
		
		print('Done')
		sys.stdout.flush()
		self.update_board_title('Done')
		
				