from game2dboard import Board
from agent import Agent
from constants import *

class Maze:
	def __init__(self, board: Board, agent: Agent, goal: tuple):
		self.board = board
		self.agent = agent
		self.goal = goal
	
	
	def start(self):
		self.board.show()