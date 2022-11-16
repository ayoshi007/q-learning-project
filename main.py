import sys
import random
from game2dboard import Board
from PIL import Image
from maze import Maze
from agent import Agent
from constants import *

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
	
	agent = None
	goal = None
	# LOOP TO TRANSLATE MAZE_CONTAINER TO OUR GAME BOARD
	# w WILL RESULT IN A WALL, f WILL RESULT IN A FREE SPACE, a WILL RESULT IN AN AGENT, g WILL RESULT IN GOAL
	for rows in MAZE_CONTAINER:
		for col in rows:
			if col == "w":
				m[r][c] = WALL_IMG_RESIZE_SRC
				c+=1
			elif col =="f":
				c+=1
			elif col =="a":
				agent = Agent(r, c)
				m[r][c] = AGENT_IMG_RESIZE_SRC
				c+=1
			elif col =="g":
				goal = (r, c)
				m[r][c] = GOAL_IMG_RESIZE_SRC
				c+=1
		r+=1
		c=0
	if not agent or not goal:
		sys.exit("No agent or goal found in maze")
	return Maze(m, agent, goal)

if __name__ == '__main__':
	#SYNTAX FOR MAZE FILE IS MAZE#, NO FILE EXTENSION
	if len(sys.argv) == 1:
		sys.exit("Usage: python maze.py <file with maze format>")
	maze_file = sys.argv[1].upper()
	if maze_file[-4:] != '.txt':
		maze_file += '.txt'
	
	board = maze_gen(MAZE_PATH + maze_file)
	board.start()

	#RUNS AGENT FOR DESIGNATED TRAINING RUNS
	for _ in range(TRAINING_RUNS):
		board.agent_begin_moving()

	#RUNS AGENT ONE LAST TIME TO EMPLOY UPDATED Q_TABLE.
	#CURRENT RETURNS NUMBER OF STEPS AGENT THINKS IS OPTIMAL AFTER X TRAINING RUNS
	print(board.agent_begin_moving())
	
	