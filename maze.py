from game2dboard import Board
from agent import Agent
import numpy as np
import pandas as pd
import random
from recording import record_metrics, record_modelhistory
from constants import *
import time

class Maze:
	def __init__(self, board: Board, agent: tuple, goal: tuple, show_gui=True):
		self.board = board
		self.agent = Agent(self, show_gui, agent[0], agent[1])
		self.goal = goal
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
				elif self.board[i - 1][j] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][NORTH] = REWARD
				
				if i == self.board.nrows - 1:
					self.rewards[i][j][SOUTH] = PUNISHMENT
				elif self.board[i + 1][j] == WALL_IMG_RESIZE_SRC:
					self.rewards[i][j][SOUTH] = PUNISHMENT
				elif self.board[i + 1][j] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][SOUTH] = REWARD
				
				if j == 0:
					self.rewards[i][j][WEST] = PUNISHMENT
				elif self.board[i][j - 1] == WALL_IMG_RESIZE_SRC:
					self.rewards[i][j][WEST] = PUNISHMENT
				elif self.board[i][j - 1] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][WEST] = REWARD
				
				if j == self.board.ncols - 1:
					self.rewards[i][j][EAST] = PUNISHMENT
				elif self.board[i][j + 1] == WALL_IMG_RESIZE_SRC:
					self.rewards[i][j][EAST] = PUNISHMENT
				elif self.board[i][j + 1] == GOAL_IMG_RESIZE_SRC:
					self.rewards[i][j][EAST] = REWARD
	
	# update agent's position and the GUI
	def update_agent_gui(self, old_pos, new_pos):
		time.sleep(SLEEP)
		self.board[old_pos[0]][old_pos[1]] = None
		if new_pos == self.goal:
			self.board[new_pos[0]][new_pos[1]] = AGENT_GOALIN_IMG_RESIZE_SRC
		else:
			self.board[new_pos[0]][new_pos[1]] = AGENT_IMG_RESIZE_SRC
		
		self.board._root.update()
	
	# used by agent to get immediate surroundings, which are a part of the agent's state
	def get_surroundings(self, r, c) -> tuple:
		surroundings = ['f', 'f', 'f', 'f']
		
		if r == 0 or self.board[r - 1][c] == WALL_IMG_RESIZE_SRC:
			surroundings[NORTH] = 'w'
		elif self.board[r - 1][c] == GOAL_IMG_RESIZE_SRC:
			surroundings[NORTH] = 'g'
			
		if r == self.board.nrows - 1 or self.board[r + 1][c] == WALL_IMG_RESIZE_SRC:
			surroundings[SOUTH] = 'w'
		elif self.board[r - 1][c] == GOAL_IMG_RESIZE_SRC:
			surroundings[NORTH] = 'g'
			
		if c == 0 or self.board[r][c - 1] == WALL_IMG_RESIZE_SRC:
			surroundings[WEST] = 'w'
		elif self.board[r][c - 1] == GOAL_IMG_RESIZE_SRC:
			surroundings[WEST] = 'g'
			
		if c == self.board.ncols - 1 or self.board[r][c + 1] == WALL_IMG_RESIZE_SRC:
			surroundings[EAST] = 'w'
		elif self.board[r][c + 1] == GOAL_IMG_RESIZE_SRC:
			surroundings[EAST] = 'g'
		
		return tuple(surroundings)
	
	def get_reward(self, r, c, action):
		return self.rewards[r][c][action]
	
	def is_goal(self, r, c):
		return self.goal == (r, c)
	
	def reset_goal(self):
		self.board[self.goal[0]][self.goal[1]] = GOAL_IMG_RESIZE_SRC
	
	def start(self, hyperparameters):
		np.seterr('raise')
		self.hyperparameters = hyperparameters
		if self.show_gui:
			self.board.on_start = self.run_hyperparameters
			self.board.show()
		else:
			self.run_hyperparameters()
	
	def run_hyperparameters(self):
		print("Starting hyperparameter runs")
		for learning_rate, epsilon, gamma, max_iter in self.hyperparameters:
			self.agent.reset_position()
			self.agent.reset_table()
			
			self.agent.set_hyperparameters(learning_rate, epsilon, gamma, max_iter)
			
			self.agent.q_train()
			test_steps = self.agent.q_test()
			record_metrics(learning_rate, epsilon, gamma, max_iter, test_steps)
			record_modelhistory(self.agent.episode_steps)
			
			#df = pd.DataFrame(data=self.agent.q_table.reshape(-1, 4), columns=list('NESW'))
			#df.to_csv("qtable.csv")
			
			if self.show_gui:
				time.sleep(1)
			
	