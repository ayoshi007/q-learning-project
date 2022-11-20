import sys
import random
import recording
from game2dboard import Board
from PIL import Image
from maze import Maze
from agent import Agent
from constants import *
from itertools import product
from recording import init_csvs

learning_rates = [.1,.5,.9]
epsilons = [.2,.5,.9] # exploit-explore 
epsilon_decay = [False,True]
random_training = [False,True]
learning_rate_decay = [False,True]
epsilon_end = .1 # For Epsilon Decay
gammas = [.9,.5,.3,.1] # discount factor
max_iters = [100,200,300]
random_training_locations= [True,False]

def main():
	#SYNTAX FOR MAZE FILE IS MAZE#, NO FILE EXTENSION
	if len(sys.argv) == 1:
		sys.exit("Usage: python maze.py <file with maze format>")
	maze_file = sys.argv[1].upper()
	show_gui = True
	if len(sys.argv) == 3 and (sys.argv[2] == '-q' or sys.argv[2] == '--quiet'):
		show_gui = False
	if maze_file[-4:] != '.txt':
		maze_file += '.txt'
	init_csvs()
	maze,testing_spots,random_spots = maze_gen(MAZE_PATH + maze_file, show_gui)
	run_model(maze,maze_file,testing_spots,random_spots)
	#RUNS AGENT ONE LAST TIME TO EMPLOY UPDATED Q_TABLE.
	#CURRENT RETURNS NUMBER OF STEPS AGENT THINKS IS OPTIMAL AFTER X TRAINING RUNS
	
	
def run_model(maze: Maze,maze_file,testing_spots,random_spots):
	maze.start(product(random_training_locations,learning_rates, epsilons, gammas, max_iters,epsilon_decay,learning_rate_decay),epsilon_end,maze_file[0:5],testing_spots,random_spots)

#FILE PARSER PLUS MAZE GENERATION
def maze_gen(file: str, show_gui: bool):
	#LIST OF LISTS THAT WILL HOLD THE MAZE AFTER IT HAS BEEN PARSED BY THE PARSER
	MAZE_CONTAINER = []

	#FILE PARSER
	#FIRST LINE IS AMOUNT OF ROWS, SECOND LINE IS AMOUNT OF COLUMNS
	with open(file, 'r') as file_object:
		ROW_LENGTH = int(file_object.readline())
		COL_LENGTH = int(file_object.readline())
		for x in file_object:
			maze_rows = [elt.strip() for elt in x.split(',')]
			MAZE_CONTAINER.append(maze_rows)
	
	#CREATES GAME BOARD
	b = Board(ROW_LENGTH,COL_LENGTH)
	b.cell_size = CELL_SIZE

	Image.open(IMG_PATH + AGENT_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + WALL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + WALL_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + GOAL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + GOAL_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + AGENT_GOALIN_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_GOALIN_IMG_RESIZE_SRC)
	Image.open(IMG_PATH + HAZARD_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + HAZARD_IMG_RESIZE_SRC)

	#VARIABLES TO ASSIST WITH CREATION OF MAZE GAMEBOARD
	r=0
	c=0
	
	testing_spawn_points = []
	random_training_locations = []
	agent = None
	goal = None
	# LOOP TO TRANSLATE MAZE_CONTAINER TO OUR GAME BOARD
	# w WILL RESULT IN A WALL, f WILL RESULT IN A FREE SPACE, a WILL RESULT IN AN AGENT, g WILL RESULT IN GOAL
	for rows in MAZE_CONTAINER:
		for col in rows:
			if col == "w":
				b[r][c] = WALL_IMG_RESIZE_SRC
			elif col =="a":
				agent = (r, c)
				random_training_locations.append((r,c))
				b[r][c] = AGENT_IMG_RESIZE_SRC
			elif col == "f":
				random_training_locations.append((r,c))
			elif col == "h":
				b[r][c] = HAZARD_IMG_RESIZE_SRC
			elif col == "s":
				testing_spawn_points.append((r,c))
				random_training_locations.append((r,c))
			elif col =="g":
				goal = (r, c)
				b[r][c] = GOAL_IMG_RESIZE_SRC
			c+=1
		r+=1
		c=0
	if not agent or not goal:
		sys.exit("No agent or goal found in maze")
	return Maze(b, agent, goal, show_gui),testing_spawn_points,random_training_locations

if __name__ == '__main__':
	main()
	