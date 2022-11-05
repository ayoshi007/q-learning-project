import random
from game2dboard import Board
from PIL import Image

CELL_SIZE = 30
IMG_PATH = 'img/'
MAZE_PATH = 'Maze/'

# ROW_LENGTH = 15
# COL_LENGTH = 20

AGENT_IMG_BASE_SRC = 'agent.png'
WALL_IMG_BASE_SRC = 'wall.png'
GOAL_IMG_BASE_SRC = 'goal.png'
AGENT_GOALIN_IMG_BASE_SRC = 'agent_goalin.png'

AGENT_IMG_RESIZE_SRC = 'agent_resize.png'
WALL_IMG_RESIZE_SRC = 'wall_resize.png'
GOAL_IMG_RESIZE_SRC = 'goal_resize.png'
AGENT_GOALIN_IMG_RESIZE_SRC = 'agent_goalin_resize.png'

#FILE PARSER PLUS MAZE GENERATION
def maze_gen(maze):
	#LIST OF LISTS THAT WILL HOLD THE MAZE AFTER IT HAS BEEN PARSED BY THE PARSER
	MAZE_CONTAINER = []

	#FILE PARSER
	#FIRST LINE IS AMOUNT OF ROWS, SECOND LINE IS AMOUNT OF COLUMNS
	with open(maze, 'r') as file_object:
		ROW_LENGTH = int(file_object.readline())
		COL_LENGTH = int(file_object.readline())
		for x in file_object:
			maze_rows = [elt.strip() for elt in x.split(',')]
			MAZE_CONTAINER.append(maze_rows)
		file_object.close()
	
	#CREATES GAME BOARD
	m = Board(ROW_LENGTH,COL_LENGTH)
	m.cell_size = CELL_SIZE

	Image.open(IMG_PATH + AGENT_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + WALL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + WALL_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + GOAL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + GOAL_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + AGENT_GOALIN_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_GOALIN_IMG_RESIZE_SRC)

	#VARIABLES TO ASSIST WITH CREATION OF MAZE GAMEBOARD
	r=0
	c=0

	#LOOP TO TRANSLATE MAZE_CONTAINER TO OUR GAME BOARD
	# w WILL RESULT IN A WALL, f WILL RESULT IN A FREE SPACE, a WILL RESULT IN AN AGENT, g WILL RESULT IN GOAL
	for rows in MAZE_CONTAINER:
		for col in rows:
			if col == "w":
				m[r][c] = WALL_IMG_RESIZE_SRC
				c+=1
			elif col =="f":
				c+=1
			elif col =="a":
				m[r][c] = AGENT_IMG_RESIZE_SRC
				c+=1
			elif col =="g":
				m[r][c] = GOAL_IMG_RESIZE_SRC
				c+=1
		r+=1
		c=0
	return m
		
# NEED TO DEFINE HOW TO REPRESENT WALLS IN MAZE
'''
class Maze:
	def __init__(self, board: Board, agent: Agent, goal: tuple, walls):
		self.board = board;
		self.agent = agent
		self.goal = goal
		self.walls = walls
	



class Agent:
	def __init__(self, starting_row=0, starting_col=0):
		self.row = starting_row
		self.col = starting_col
	
	def move_up():
		self.row -= 1
	def move_down():
		self.row += 1
	def move_right():
		self.col += 1
	def move_left():
		self.col -= 1
'''

if __name__ == '__main__':
	#SYNTAX FOR MAZE FILE IS MAZE#, NO FILE EXTENSION 
	b = maze_gen(MAZE_PATH+input("Which Maze would you like to generate?").upper()+".txt")
	b.show()
	'''
	b = Board(15, 20)
	b.cell_size = CELL_SIZE

	Image.open(IMG_PATH + AGENT_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + WALL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + WALL_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + GOAL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + GOAL_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + AGENT_GOALIN_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_GOALIN_IMG_RESIZE_SRC)

	b[0][0] = AGENT_IMG_RESIZE_SRC
	b[0][1] = WALL_IMG_RESIZE_SRC
	b[GOAL_ROW_LOCATION][GOAL_COL_LOCATION] = GOAL_IMG_RESIZE_SRC
	
	NEED TO CREATE MAZE GENERATION ALGORITHM TO CREATE MAZE
	'''