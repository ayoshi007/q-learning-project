from game2dboard import Board
from agent import Agent
import numpy as np
import random
# from numba import jit,cuda
from constants import *

class Maze:
	def __init__(self, board: Board, agent: Agent, goal: tuple):
		self.board = board
		self.agent = agent
		self.goal = goal
	
	
	def start(self):
		self.agent.getting_number_of_states(self.board)
		self.board.show()
	
	#RENFORCEMENT LEARNER
	# @jit(target_backend ='cuda')
	def agent_training(self,lr:tuple,gamma:tuple,epsilon:tuple):
		done = False
		steps = 0
		while not done:
			state = self.agent.get_state(self.board)
			if random.uniform(0,1) < epsilon:
				action = random.randint(0,3)
			else:
				action = np.argmax(self.agent.get_qtable()[state])
			reward, done = self.agent.move(self.board,action)

			new_state = self.agent.get_state(self.board)
			self.agent.table_update(state,action,lr,gamma,reward,new_state)
			steps = steps + 1
		self.agent.reset_position()
		return steps
	# @jit(target_backend ='cuda')
	def agent_test(self,lr:tuple,gamma:tuple,epsilon:tuple):
		done = False
		steps = 0
		while not done:
			state = self.agent.get_state(self.board)
			if random.uniform(0,1) < epsilon:
				action = random.randint(0,3)
			else:
				action = np.argmax(self.agent.get_qtable()[state])
			reward, done = self.agent.move(self.board,action)

			new_state = self.agent.get_state(self.board)
			self.agent.table_update(state,action,lr,gamma,reward,new_state)
			steps = steps + 1
		#print(self.agent.table_output())
		self.agent.reset_position()
		self.agent.reset_table()
		return steps
