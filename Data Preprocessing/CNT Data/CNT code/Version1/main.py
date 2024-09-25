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
			   'nback1', 'nback2']
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
		for cond in [1, 0]:
			number = (df.loc[:, columns[1]] == cond).sum()
			correct = (df[(df.loc[:, columns[1]] == cond) & (df.loc[:, columns[2]] == 1)]).shape[0]
			wrong = (df[(df.loc[:, columns[1]] == cond) & (df.loc[:, columns[2]] == 0)]).shape[0]
			group_df = sum = df.groupby(columns[1]).agg({columns[6]: ['sum', 'median', 'min', 'max', 'std']})['Reaction time']
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
	

def main():
	# Get ID
	for dir in os.listdir(args.dir):
		if '0.00' in dir:
			id = dir[:4]
	writer = pd.ExcelWriter(f'CNT_{id}.xlsx', engine='xlsxwriter')
	for (path, dir, files) in sorted(os.walk(args.dir)):
		level = -1
		if '0.00' in path:
			level = 0
		elif '0.03' in path:
			level = 0.03
		elif '0.07' in path:
			level = 0.07

		for file in files:
			if 'NB' in file:
				Nback(os.path.join(path, file), level, writer)
	writer.save()

if __name__ == '__main__':
	main()