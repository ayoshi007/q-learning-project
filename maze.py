import randomfrom game2dboard import Boardfrom PIL import ImageCELL_SIZE = 30IMG_PATH = 'img/'ROW_LENGTH = 15COL_LENGTH = 20AGENT_IMG_BASE_SRC = 'agent.png'WALL_IMG_BASE_SRC = 'wall.png'GOAL_IMG_BASE_SRC = 'goal.png'AGENT_GOALIN_IMG_BASE_SRC = 'agent_goalin.png'AGENT_IMG_RESIZE_SRC = 'agent_resize.png'WALL_IMG_RESIZE_SRC = 'wall_resize.png'GOAL_IMG_RESIZE_SRC = 'goal_resize.png'AGENT_GOALIN_IMG_RESIZE_SRC = 'agent_goalin_resize.png'# NEED TO DEFINE HOW TO REPRESENT WALLS IN MAZEclass Maze:	def __init__(self, board: Board, agent: Agent, goal: tuple, walls):		self.board = board;		self.agent = agent		self.goal = goal		self.walls = walls	class Agent:	def __init__(self, starting_row=0, starting_col=0):		self.row = starting_row		self.col = starting_col		def move_up():		self.row -= 1	def move_down():		self.row += 1	def move_right():		self.col += 1	def move_left():		self.col -= 1	if __name__ == '__main__':	b = Board(15, 20)	b.cell_size = CELL_SIZE	Image.open(IMG_PATH + AGENT_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_IMG_RESIZE_SRC)	Image.open(IMG_PATH + WALL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + WALL_IMG_RESIZE_SRC)	Image.open(IMG_PATH + GOAL_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + GOAL_IMG_RESIZE_SRC)	Image.open(IMG_PATH + AGENT_GOALIN_IMG_BASE_SRC).resize((CELL_SIZE, CELL_SIZE)).save(IMG_PATH + AGENT_GOALIN_IMG_RESIZE_SRC)	b[0][0] = AGENT_IMG_RESIZE_SRC	b[0][1] = WALL_IMG_RESIZE_SRC	b[random.randint(0, ROW_LENGTH - 1)][random.randint(0, COL_LENGTH - 1)] = GOAL_IMG_RESIZE_SRC		# NEED TO CREATE MAZE GENERATION ALGORITHM TO CREATE MAZE			b.show()