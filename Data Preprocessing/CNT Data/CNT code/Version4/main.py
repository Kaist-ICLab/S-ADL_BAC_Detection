import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, required=True)
args = parser.parse_args()

def Nback(file, level, writer):
	columns = ['Trial number', 'Type of trial (1=a matching stimulus ; 0=a non-matching stimulus)',
			   'Score (1 means correct, 0 means incorrect)', 'Match',
			   'Miss', 'False Alarm', 'Reaction time', 'Memory',
			   'Current letter (the current letter, a number between 1 and 15, representing letterA, etc)',
			   'nback1', 'nback2', 'nback3']
	# Load data
	with open(file) as f:
		lst1 = []
		lst2 = []
		lst3 = []
		total_lst = []
		for line in f.readlines():
			line = line.strip()
			line = line.split(' ')
			if line[0] == '1':
				lst1.append(line[1:])
			if line[0] == '2':
				lst2.append(line[1:])
			if line[0] == '3':
				lst3.append(line[1:])
			total_lst.append(line[1:])

	row = 0
	for idx, lst in enumerate([lst1, lst2, lst3, total_lst]):
		df = pd.DataFrame(lst)
		df.columns = columns
		df = df.astype(int)
		lst = []
		for cond in [0, 1]:
			number = (df.loc[:, columns[1]] == cond).sum()
			correct = (df[(df.loc[:, columns[1]] == cond) & (df.loc[:, columns[2]] == 1)]).shape[0]
			wrong = (df[(df.loc[:, columns[1]] == cond) & (df.loc[:, columns[2]] == 0)]).shape[0]
			group_df = df.groupby(columns[1]).agg({columns[6]: ['sum', 'median', 'min', 'max', 'std']})['Reaction time']
			sum = group_df['sum'][cond]
			median = group_df['median'][cond]
			min = group_df['min'][cond]
			max = group_df['max'][cond]
			std = group_df['std'][cond]
			cond = [number, correct, wrong, sum, median, min, max, std]
			lst.append(cond)

		if idx != 3:
			df_condition = pd.DataFrame(lst)
			df_condition.columns = ['number', 'correct', 'wrong', 'sum', 'median', 'min', 'max', 'std']

			# Write data to excel
			df.to_excel(writer, sheet_name=f'Nback_{level}', startrow=row)
			row += len(df.index) + 1
		else:
			last_lst = []
			for idx, cond in enumerate(lst):
				error_rate = lst[idx][2] / float(lst[idx][0]) * 100
				mean = lst[idx][3] / lst[idx][0]
				last_cond = lst[idx][0:3]
				last_cond.append(error_rate)
				last_cond.append(mean)
				last_cond += lst[idx][4:]
				last_lst.append(last_cond)
			df_condition = pd.DataFrame(last_lst)
			df_condition.columns = ['trial', 'correct', 'wrong', 'error rate', 'mean', 'median', 'min', 'max', 'std']

		df_condition.to_excel(writer, sheet_name=f'Nback_{level}', startrow=row)
		row += len(df_condition.index) + 2
	return
	
def Stroop(file, level, writer):
	columns = ['name of word', 'color word is printed in', 
			   'Stroop color match (1=compatible, 0=incompatible)',
			   'tablerow number', 'the pressed key number',
			   'Status (1=correct, 2=wrong, 3=timeout)',
			   'Response time (milliseconds)']
	# Load data
	with open(file) as f:
		lst = []
		for line in f.readlines():
			line = line.strip()
			line = line.split(' ')
			line = list(filter(None, line))
			lst.append(line[1:])
	row = 0
	df = pd.DataFrame(lst)
	for i in range(2, 7):
		df.loc[:, i] = df.loc[:, i].astype(int)
	df.columns = columns
	lst = []
	for cond in [0, 1]:
		trial = (df.loc[:, columns[2]] == cond).sum()
		group_df = df.groupby(columns[2]).agg({columns[6]: ['mean', 'median', 'min', 'max', 'std']})[columns[6]]
		mean = group_df['mean'][cond]
		median = group_df['median'][cond]
		min = group_df['min'][cond]
		max = group_df['max'][cond]
		correct = (df[(df.loc[:, columns[2]] == cond) & (df.loc[:, columns[5]] == 1)]).shape[0]
		error_rate = float(trial - correct) / trial * 100
		std = group_df['std'][cond]
		cond = [trial, mean, median, min, max, error_rate, correct, std]
		lst.append(cond)

	df_condition = pd.DataFrame(lst)
	df_condition.columns = ['trial', 'mean', 'median', 'min', 'max', 'error rate', 'correct', 'std']

	# Write data to excel
	df.to_excel(writer, sheet_name=f'Stroop_{level}', startrow=row)
	row += len(df.index) + 1
	df_condition.to_excel(writer, sheet_name=f'Stroop_{level}', startrow=row)
	return

def Switching(file, level, writer):
	columns = ['BlocknameTask-typeCongruent or incongruent(as word)',
			   '1', '2', 'Congruent or incongruent (as number 1 or 2)',
			   'Required button press (left = b-key, right = n-key)',
			   'Response time in milliseconds', 'Status (1=correct, 2=wrong, 3=timeout)',
			   'Taskswitching']

	# Load data
	with open(file) as f:
		lst = []
		for line in f.readlines():
			line = line.strip()
			line = line.split(' ')
			line = list(filter(None, line))
			lst.append(line)

	row = 0
	df = pd.DataFrame(lst)
	for i in [3, 5, 6, 7]:
		df.loc[:, i] = df.loc[:, i].astype(int)
	df.columns = columns
	lst = []
	for cong in [1, 2]:
		for cond in [1, 2]:
			trials = (df[(df.loc[:, columns[3]] == cong) & (df.loc[:, columns[7]] == cond)]).shape[0]
			group_df = df.groupby([columns[3], columns[7]]).agg({columns[5]: ['mean', 'median', 'min', 'max', 'std']})[columns[5]]
			mean = group_df['mean'][(cong, cond)]
			median = group_df['median'][(cong, cond)]
			min = group_df['min'][(cong, cond)]
			max = group_df['max'][(cong, cond)]
			correct = (df[(df.loc[:, columns[3]] == cong) & 
						  (df.loc[:, columns[7]] == cond) &
						  (df.loc[:, columns[6]] == 1)]).shape[0]
			error_rate = float(trials - correct) / trials * 100
			std = group_df['std'][(cong, cond)]
			cond = [trials, mean, median, min, max, error_rate, correct, std]
			lst.append(cond)

	lst[0].append('condition 1_congruent')
	lst[1].append('condition 2_congruent')
	lst[2].append('condition 1_incongruent')
	lst[3].append('condition 2_incongruent')
	df_condition = pd.DataFrame(lst)
	df_condition.columns = ['trials', 'mean', 'median', 'min', 'max', 'error rate', 'correct', 'std', 'index_title']
	df_condition = df_condition.set_index('index_title')

	# Write data to excel
	df.to_excel(writer, sheet_name=f'Switching_{level}', startrow=row)
	row += len(df.index) + 1
	df_condition.to_excel(writer, sheet_name=f'Switching_{level}', startrow=row)
	return

def Wcst(file, level, writer):
	columns = ['the card shown', 'the card that should be clicked of the top four on screen',
	 		   'the card that would be clicked if the participant is persevering',
			   'the trial in a sequence', 'name of the task', 'detailed card description:shape',
			   'detailed card description: number of symbols on the card',
			   'detailed card description: color', 'Reaction time in milliseconds',
			   'Status', 'the card that was actually clicked', 'If 1, this trial was an error (otherwise 0)',
			   'If 1, this trial was a perseveration error (otherwise 0)', 
			   'If 1, this trial was not a perseveration error (otherwise 0)']
	# Load data
	with open(file) as f:
		lst = []
		for line in f.readlines():
			line = line.strip()
			line = line.split(' ')
			line = list(filter(None, line))
			lst.append(line)
	row = 0
	df = pd.DataFrame(lst)
	for i in [0, 1, 2, 3, 6, 8, 9, 10, 11, 12, 13]:
		df.loc[:, i] = df.loc[:, i].astype(int)
	df.columns = columns

	lst = []
	trial = len(df.index)
	mean = df.mean(axis=0)[columns[8]]
	median = df.median(axis=0)[columns[8]]
	min = df.min(axis=0)[columns[8]]
	max = df.max(axis=0)[columns[8]]
	correct = (df[(df.loc[:, columns[9]] == 1)]).shape[0]
	error_rate = float(trial - correct) / trial * 100
	std = df.std(axis=0)[columns[8]]
	data = [trial, mean, median, min, max, error_rate, correct, std]
	lst.append(data)

	df_condition = pd.DataFrame(lst)
	df_condition.columns = ['trial', 'mean', 'median', 'min', 'max', 'error rate', 'correct', 'std']

	# Write data to excel
	df.to_excel(writer, sheet_name=f'Wcst_{level}', startrow=row)
	row += len(df.index) + 1
	df_condition.to_excel(writer, sheet_name=f'Wcst_{level}', startrow=row)
	return

def Sart(file, level, writer):
	columns = ['name of block', 'number of block', 'go (1) or no go(0)',
			   'digit (1~9)', 'size of stimulus (1~5)', 'response outcome (0 error, 1 correct)',
			   'reaction time in ms']
	
	# Load data
	with open(file) as f:
		lst = []
		for line in f.readlines():
			line = line.strip()
			line = line.split(' ')
			line = list(filter(None, line))
			lst.append(line)

	row = 0
	df = pd.DataFrame(lst)
	for i in range(1, 7):
		df.loc[:, i] = df.loc[:, i].astype(int)
	df.columns = columns

	lst = []
	for cond in [0, 1]:
		trial = (df.loc[:, columns[2]] == cond).sum()
		group_df = df.groupby(columns[2]).agg({columns[6]: ['mean', 'min', 'median', 'max', 'std']})[columns[6]]
		mean = group_df['mean'][cond]
		median = group_df['median'][cond]
		min = group_df['min'][cond]
		max = group_df['max'][cond]
		std = group_df['std'][cond]
		correct = (df[(df.loc[:, columns[2]] == cond) & (df.loc[:, columns[5]] == 1)]).shape[0]
		error_rate = float(trial - correct) / trial * 100
		cond = [trial, mean, median, min, max, error_rate, correct, std]
		lst.append(cond)

	df_condition = pd.DataFrame(lst)
	df_condition.columns = ['trial', 'mean', 'median', 'min', 'max', 'error rate', 'correct', 'std']

	# Write data to excel
	df.to_excel(writer, sheet_name=f'Sart_{level}', startrow=row)
	row += len(df.index) + 1
	df_condition.to_excel(writer, sheet_name=f'Sart_{level}', startrow=row)
	return 

def main():
	# Get ID
	for dir in os.listdir(args.dir):
		if '0.00' in dir:
			id = dir[:4]
	writer = pd.ExcelWriter(f'CNT_{id}.xlsx', engine='xlsxwriter')
	dummy = pd.DataFrame()
	for task in ['Nback', 'Stroop', 'Switching', 'Wcst', 'Sart']:
		for level in ['0', '0.03', '0.07']:
			dummy.to_excel(writer, sheet_name=f'{task}_{level}')

	level0_cnt = 0
	for (path, dir, files) in sorted(os.walk(args.dir)):
		level = -1
		if '0.00' in path:
			if level0_cnt > 0:
				level = f'0_{level0_cnt}'
			else:
				level = 0
			level0_cnt += 1
		elif '0.03' in path:
			level = 0.03
		elif '0.07' in path:
			level = 0.07

		for file in files:
			if 'NB' in file:
				Nback(os.path.join(path, file), level, writer)
			if 'ST' in file:
				Stroop(os.path.join(path, file), level, writer)
			if 'TS' in file:
				Switching(os.path.join(path, file), level, writer)
			if 'WS' in file:
				Wcst(os.path.join(path, file), level, writer)
			if 'SR' in file:
				Sart(os.path.join(path, file), level, writer)
	writer.save()

if __name__ == '__main__':
	main()
