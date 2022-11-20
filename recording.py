from constants import *
from datetime import datetime

now = datetime.now()
datetimestamp = f'{now.date()}_{now.hour:02}-{now.minute:02}-{now.second:02}'
METRICS_CSV = f'model_metrics_{datetimestamp}.csv'
MODELHISTORY_CSV = f'model_histories_{datetimestamp}.csv'
REWARDHISTORY_CSV = f'reward_histories_{datetimestamp}.csv'

#INITIALIZES OUR CSVS
def init_csvs():
	file = open(METRICS_CSV,'w')
	file.write(METRIC_COLUMNS)
	file.write('\n')
	file.close()
	file = open(MODELHISTORY_CSV, 'w')
	file.close()
	file = open(REWARDHISTORY_CSV,'w')
	file.close()

#FILLS OUR MODEL_METRICS
def record_metrics(maze_file,random_training,learn_rate,lr_decay, epsilon,epsilon_end,epsilon_decay, gamma, max_iter, test_steps,test_reward,train_step_avg,train_reward_avg):
	metrics_file = open(METRICS_CSV, 'a')
	metrics_file.write(f'{maze_file},{random_training},{learn_rate},{lr_decay},{epsilon},{epsilon_end},{epsilon_decay},{gamma},{max_iter},{test_steps[0]},{test_steps[1]},{test_steps[2]},')
	metrics_file.write(f'{test_steps[3]},{test_reward[0]},{test_reward[1]},{test_reward[2]},{test_reward[3]},{sum(test_steps)},{sum(test_reward)},{train_step_avg:.2f},{train_reward_avg:.2f}')
	metrics_file.write('\n')
	metrics_file.close()

def record_modelhistory(step_history):
	modelhistory = open(MODELHISTORY_CSV,'a')
	modelhistory_str = ','.join([str(x) for x in step_history])
	modelhistory.write(modelhistory_str)
	modelhistory.write('\n')
	modelhistory.close()
	modelhistory = None

def record_rewardhistory(reward_history):
	rewardhistory = open(REWARDHISTORY_CSV,'a')
	rewardhistory_str = ','.join([str(x) for x in reward_history])
	rewardhistory.write(rewardhistory_str)
	rewardhistory.write('\n')
	rewardhistory.close()
	rewardhistory = None