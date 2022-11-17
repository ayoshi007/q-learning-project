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

learning_rates = [.2]
epsilons = [.15] # exploit-explore 
gammas = [.9] # discount factor
max_iters = [200]

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
	maze = maze_gen(MAZE_PATH + maze_file, show_gui)
	run_model(maze)
	#RUNS AGENT ONE LAST TIME TO EMPLOY UPDATED Q_TABLE.
	#CURRENT RETURNS NUMBER OF STEPS AGENT THINKS IS OPTIMAL AFTER X TRAINING RUNS
	
	
def run_model(maze: Maze):
	maze.start(product(learning_rates, epsilons, gammas, max_iters))

#INITIALIZES OUR CSVS
def init_csvs():
	file = open(METRICS_CSV,'w')
	file.write(METRIC_COLUMNS)
	file.write('\n')
	file.close()
	file = open(MODELHISTORY_CSV, 'w')
	file.close()

#FILLS OUR MODEL_METRICS
def metric_creator(max_iters:tuple,test_steps:tuple):
	metrics_file = open(METRICS_CSV, 'a')
	metrics_file.write(f'{LEARNING_RATE},{EPSILON},{GAMMA},{max_iters},{test_steps}')
	metrics_file.write('\n')
	metrics_file.close()

#PREFORMS REINFORMENT LEARNING AND TRACKS STEPS TAKEN PER ITERATIONS
def reinforcement_learning(x:tuple):
	training_list =[]
	#RUNS AGENT FOR DESIGNATED TRAINING RUNS
	for _ in range(x):
		steps = board.agent_training()
		training_list.append(steps)
	modelhistory = open(MODELHISTORY_CSV,'a')
	modelhistory_str = ','.join([str(x) for x in training_list])
	modelhistory.write(modelhistory_str)
	modelhistory.write('\n')
	modelhistory.close()
	modelhistory_str = None
	test_steps = board.agent_test()
	metric_creator(x,test_steps)
	
	training_list = []


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
				b[r][c] = AGENT_IMG_RESIZE_SRC
			elif col =="g":
				goal = (r, c)
				b[r][c] = GOAL_IMG_RESIZE_SRC
			c+=1
		r+=1
		c=0
	if not agent or not goal:
		sys.exit("No agent or goal found in maze")
	return Maze(b, agent, goal, show_gui)

if __name__ == '__main__':
	main()
	