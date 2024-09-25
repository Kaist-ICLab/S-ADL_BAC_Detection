import pandas as pd
import argparse
import json
from datetime import datetime, timedelta
from functools import reduce

init_time = 0

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, default='./result.csv', help='CSV file path')
parser.add_argument('--reqs', type=str, default='./sample_phone_register.txt', help='Request file path')
args = parser.parse_args()

def parse_reqs(file):
    res = []
    with open(file, 'r') as f:
        res = list(map(lambda s: s.rstrip(), f.readlines()))
    return res
    

def main():
    reqs = parse_reqs(args.reqs)
    df = pd.read_csv(args.file)
    df.columns = ['id', 'datumType', 'offsetTimestamp', 'offsetUploadTime',
                  'subject', 'timestamp', 'uploadTime', 'utfOffsetSec',
                  'value']
    df['offsetTimestamp'] = pd.to_datetime(df['offsetTimestamp'], format='%Y-%m-%dT%H:%M:%S.%fZ')
    df = df.sort_values(by=['timestamp'])

    enter_init = False
    prev_time_idx= 'offsetTimestamp'
    finish_time_idx= 'offsetTimestamp'
    if reqs[0][-1] == 'Z': 
        prev_time = datetime.strptime(reqs[0], '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        prev_time = reqs[0]
        prev_time_idx = 'timestamp'

    if reqs[1][-1] == 'Z':
        finish_time = datetime.strptime(reqs[1], '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        finish_time = reqs[1]
        finish_time_idx = 'timestamp'

    find_rows = pd.DataFrame()
    find_rows_id = list()
    df_dict = dict()

    for idx, row in df.iterrows():
        if str(row[finish_time_idx]) > str(finish_time):
            break

        # Find init time
        if not enter_init:
            if str(row[prev_time_idx]) >= str(prev_time):
                prev_time = init_time
                enter_init = True
            else:
                continue

        find = False
        for req in reqs[3:]:
            # Find specified event
            req = req.split('-')
            value = json.loads(row['value'])

            if row['datumType'].lower() == req[0].lower():
                if len(req) == 1:
                    find = True
                else:
                    if ('type' in value.keys() and value['type'].lower() == req[1].lower()) or\
                    ('packageName' in value.keys() and value['packageName'].lower() == req[1].lower()) or\
                    ('isPosted' in value.keys() and str(value['isPosted']).lower() == req[1].lower()) or\
                    ('messageBox' in value.keys() and value['messageBox'].lower() == req[1].lower()):
                        if len(req) == 2:    
                            find = True
                        elif ('type' in value.keys() and value['type'].lower() == req[2].lower()) or\
                        ('isPosted' in value.keys() and str(value['isPosted']).lower() == req[2].lower()):
                            find = True

            if find:
                info = dict()
                for target in ['packageName', 'type', 'isPosted', 'messageBox', 'currentKey', 'prevKey', 'timeTaken']:
                    if target in value.keys(): 
                        info[target] = value[target]
                
                tmp = row.loc[['datumType', 'offsetTimestamp', 'timestamp']]
                tmp['value'] = info
                tmp['offsetTimestamp'] = str(tmp['offsetTimestamp'])[:10] + 'T' + str(tmp['offsetTimestamp'])[11:] + '.000Z'
                tmp['timestamp'] = str(tmp['timestamp']) + ''
                find_rows = find_rows.append(tmp)

                id = '_'.join(req)
                find_rows_id.append(id)
                if id in df_dict.keys():
                    df_dict[id] = (df_dict[id][0], df_dict[id][1] + 1)
                else:
                    df_dict[id] = (0, 1)
                break
    for (idx, row), id in zip(find_rows.iterrows(), find_rows_id):
        df_dict[id] = (df_dict[id][0] + 1, df_dict[id][1])
        cnt, total_cnt = df_dict[id]

        find_rows.loc[idx, 'count'] = f'{cnt} / {total_cnt}'

    req_columns = reqs[2].split(',')
    req_columns = list(map(lambda s: s.strip(), req_columns))
    all_columns = ['offsetTimestamp', 'timestamp', 'value', 'datumType', 'count']
    for column in all_columns:
        if column not in req_columns:
            req_columns.append(column)

    find_rows = find_rows[req_columns]
    print(find_rows.to_string())
    find_rows.to_excel('result.xlsx', encoding='utf-8')

if __name__ == '__main__':
    main()
