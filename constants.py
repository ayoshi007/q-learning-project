CELL_SIZE = 30
IMG_PATH = 'img/'
MAZE_PATH = 'Maze/'

METRICS_CSV = 'model_metrics.csv'
MODELHISTORY_CSV = 'model_histories.csv'
REWARDHISTORY_CSV = 'reward_histories.csv'
METRIC_COLUMNS = 'maze_number,random_training,learning_rate,lr_decay,epsilon,epsilon_end,epsilon_decay,gamma,max_iters,test1_steps,test2_steps,test3_steps,test4_steps,test1_reward_sum,test2_reward_sum,test3_reward_sum,test4_reward_sum,test_step_sum,test_reward_sum,train_step_average,train_reward_average'

AGENT_IMG_BASE_SRC = 'agent.png'
WALL_IMG_BASE_SRC = 'wall.png'
GOAL_IMG_BASE_SRC = 'goal.png'
AGENT_GOALIN_IMG_BASE_SRC = 'agent_goalin.png'
HAZARD_IMG_BASE_SRC = 'hazard.png'
AGENT_IN_HAZARD_IMG_BASE_SRC = 'agent_in_hazard.png'

AGENT_IMG_RESIZE_SRC = 'agent_resize.png'
WALL_IMG_RESIZE_SRC = 'wall_resize.png'
GOAL_IMG_RESIZE_SRC = 'goal_resize.png'
AGENT_GOALIN_IMG_RESIZE_SRC = 'agent_goalin_resize.png'
HAZARD_IMG_RESIZE_SRC = 'hazard_resize.png'
AGENT_IN_HAZARD_IMG_RESIZE_SRC = 'agent_in_hazard_resize.png'


PUNISHMENT = -25
REWARD = 5000
FREE_MOVEMENT_PENALTY = -5
HAZARD_PUNISHMENT = -50

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

SLEEP = 0.00001