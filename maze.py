from game2dboard import Board
from agent import Agent
import numpy as np
import random
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
	def agent_training(self):
		done = False
		steps = 0
		while not done:
			state = self.agent.get_state(self.board,self.goal)
			if random.uniform(0,1) < EPSILON:
				action = random.randint(0,3)
			else:
				action = np.argmax(self.agent.get_qtable()[state])
			reward, done = self.agent.move(self.board,action)

			new_state = self.agent.get_state(self.board,self.goal)
			self.agent.table_update(state,action,reward,new_state)
			steps = steps + 1
		#print(self.agent.table_output())
		self.agent.reset_position()
		return steps

	def agent_test(self):
		done = False
		steps = 0
		while not done:
			state = self.agent.get_state(self.board,self.goal)
			if random.uniform(0,1) < EPSILON:
				action = random.randint(0,3)
			else:
				action = np.argmax(self.agent.get_qtable()[state])
			reward, done = self.agent.move(self.board,action)

			new_state = self.agent.get_state(self.board,self.goal)
			self.agent.table_update(state,action,reward,new_state)
			steps = steps + 1
		#print(self.agent.table_output())
		self.agent.reset_position()
		self.agent.reset_table()
		return steps
