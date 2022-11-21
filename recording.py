from constants import *
from datetime import datetime

now = datetime.now()
datetimestamp = f'{now.date()}_{now.hour:02}-{now.minute:02}-{now.second:02}'
METRICS_CSV = f'model_metrics_{datetimestamp}.csv'
MODELHISTORY_CSV = f'model_histories_{datetimestamp}.csv'
REWARDHISTORY_CSV = f'reward_histories_{datetimestamp}.csv'
METRIC_COLUMNS_BEFORE = 'maze_number,random_training,learning_rate,lr_decay,epsilon,epsilon_end,epsilon_decay,gamma,max_iters,'
METRIC_COLUMNS_AFTER = 'test_step_sum,test_reward_sum,train_step_average,train_reward_average'


#INITIALIZES OUR CSVS
def init_csvs(testing_spot_count):
	file = open(METRICS_CSV,'w')
	file.write(METRIC_COLUMNS_BEFORE)
	file.write(','.join([f'test{i + 1}_success' for i in range(testing_spot_count)]))
	file.write(',')
	file.write(','.join([f'test{i + 1}_steps' for i in range(testing_spot_count)]))
	file.write(',')
	file.write(','.join([f'test{i + 1}_reward_sum' for i in range(testing_spot_count)]))
	file.write(',')
	file.write(METRIC_COLUMNS_AFTER)
	file.write('\n')
	file.close()
	file = open(MODELHISTORY_CSV, 'w')
	file.close()
	file = open(REWARDHISTORY_CSV,'w')
	file.close()

#FILLS OUR MODEL_METRICS
def record_metrics(maze_file, random_training, learn_rate, lr_decay, epsilon, epsilon_end, epsilon_decay, gamma, max_iter,test_cr ,test_steps, test_reward, train_step_avg, train_reward_avg):
	metrics_file = open(METRICS_CSV, 'a')
	test_cr_str = ','.join([str(s) for s in test_cr])
	test_steps_str = ','.join([str(s) for s in test_steps])
	test_reward_str = ','.join([str(s) for s in test_reward])
	metrics_file.write(f'{maze_file},{random_training},{learn_rate},{lr_decay},{epsilon},{epsilon_end},{epsilon_decay},{gamma},{max_iter},')
	metrics_file.write(f'{test_cr_str},{test_steps_str},{test_reward_str},{sum(test_steps)},{sum(test_reward)},{train_step_avg:.2f},{train_reward_avg:.2f}')
	metrics_file.write('\n')
	metrics_file.close()

def record_modelhistory(step_history):
	modelhistory = open(MODELHISTORY_CSV,'a')
	modelhistory_str = ','.join([str(x) for x in step_history])
	modelhistory.write(modelhistory_str)
	modelhistory.write('\n')
	modelhistory.close()

def record_rewardhistory(reward_history):
	rewardhistory = open(REWARDHISTORY_CSV,'a')
	rewardhistory_str = ','.join([str(x) for x in reward_history])
	rewardhistory.write(rewardhistory_str)
	rewardhistory.write('\n')
	rewardhistory.close()