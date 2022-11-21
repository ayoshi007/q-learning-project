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

learning_rates = [.01, .05, .1, .5, .9]
epsilons = [.3, .5, .9] # exploit-explore
epsilon_end = [.01] # For Epsilon Decay
gammas = [.5, .7, .9] # discount factor
max_iters = [100, 200, 300]
epsilon_decay = [True, False]
learning_rate_decay = [True, False]
random_training = [True, False]

repeats = 1

def main():
	#SYNTAX FOR MAZE FILE IS MAZE#, NO FILE EXTENSION
	if len(sys.argv) == 1:
		sys.exit("Usage: python maze.py <file with maze format>")
	maze_file = sys.argv[1].upper()
	show_gui = True
	options = sys.argv[2:]
	if '-q' in options or '--quiet' in options:
		show_gui = False
	if '-nr' in options or '--no-reporting' in options:
		show_gui = None
		
	if maze_file[-4:] != '.txt':
		maze_file += '.txt'
	maze = maze_gen(MAZE_PATH + maze_file, show_gui)
	init_csvs(len(maze.testing_spots))
	run_model(maze)
	#RUNS AGENT ONE LAST TIME TO EMPLOY UPDATED Q_TABLE.
	#CURRENT RETURNS NUMBER OF STEPS AGENT THINKS IS OPTIMAL AFTER X TRAINING RUNS
	

def run_model(maze: Maze):
	hyperparam_combos = product(learning_rates, epsilons, epsilon_end, gammas, max_iters, epsilon_decay, learning_rate_decay, random_training)
	total_runs = len(learning_rates) * len(epsilons) * len(epsilon_end) * len(gammas) * len(max_iters) * len(epsilon_decay) * len(learning_rate_decay) * len(random_training) * repeats
	maze.start(hyperparam_combos, repeats, total_runs)

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
	Image.open(IMG_PATH + AGENT_IN_HAZARD_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_IN_HAZARD_IMG_RESIZE_SRC)

	#VARIABLES TO ASSIST WITH CREATION OF MAZE GAMEBOARD
	r=0
	c=0
	
	testing_spawn_points = []
	random_training_locations = []
	agent = None
	goals = set()
	# LOOP TO TRANSLATE MAZE_CONTAINER TO OUR GAME BOARD
	# w WILL RESULT IN A WALL, f WILL RESULT IN A FREE SPACE, a WILL RESULT IN AN AGENT, g WILL RESULT IN GOAL
	for r, rows in enumerate(MAZE_CONTAINER):
		for c, col in enumerate(rows):
			if col == 'w':
				b[r][c] = WALL_IMG_RESIZE_SRC
			elif col == 'g':
				goals.add((r, c))
				b[r][c] = GOAL_IMG_RESIZE_SRC
			else:
				random_training_locations.append((r,c))
				if 's' in col:
					testing_spawn_points.append((r,c))
				if 'a' in col:
					agent = (r, c)
					b[r][c] = AGENT_IMG_RESIZE_SRC
				elif 'h' in col:
					b[r][c] = HAZARD_IMG_RESIZE_SRC
	
	if not agent or not goals:
		sys.exit("No agent or goal found in maze")
	return Maze(file[len(MAZE_PATH):-4], b, agent, goals, random_training_locations, testing_spawn_points, show_gui)

print("Hello")
if __name__ == '__main__':
	main()
	