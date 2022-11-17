from constants import *

#INITIALIZES OUR CSVS
def init_csvs():
	file = open(METRICS_CSV,'w')
	file.write(METRIC_COLUMNS)
	file.write('\n')
	file.close()
	file = open(MODELHISTORY_CSV, 'w')
	file.close()

#FILLS OUR MODEL_METRICS
def record_metrics(learn_rate, epsilon, gamma, max_iter, test_steps):
	metrics_file = open(METRICS_CSV, 'a')
	metrics_file.write(f'{learn_rate},{epsilon},{gamma},{max_iter},{test_steps}')
	metrics_file.write('\n')
	metrics_file.close()

def record_modelhistory(step_history):
	modelhistory = open(MODELHISTORY_CSV,'a')
	modelhistory_str = ','.join([str(x) for x in step_history])
	modelhistory.write(modelhistory_str)
	modelhistory.write('\n')
	modelhistory.close()
	