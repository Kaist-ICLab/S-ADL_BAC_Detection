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
    
def get_unique_id(row):
    output = row['datumType']
    value = json.loads(row['value'])

    for k, v in value.items():
        output += ' - '
        output += str(v)

    return output

def main():
    reqs = parse_reqs(args.reqs)
    df = pd.read_csv(args.file)
    df.columns = ['id', 'datumType', 'offsetTimestamp', 'offsetUploadTime',
                  'subject', 'timestamp', 'uploadTime', 'utfOffsetSec',
                  'value']
    df['offsetTimestamp'] = pd.to_datetime(df['offsetTimestamp'], format='%Y-%m-%dT%H:%M:%S.%fZ')
    df = df.sort_values(by=['timestamp'])
    df = df.drop_duplicates(['timestamp'])

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
        for req in reqs[2:]:
            # Find specified event
            value = json.loads(row['value'])

            if str(row['timestamp']) == str(req):
                find = True
                id = get_unique_id(row)
                if id in df_dict.keys():
                    df_dict[id] = (df_dict[id][0], df_dict[id][1] + 1)
                else:
                    df_dict[id] = (0, 1)
                
                info = dict()
                for target in ['packageName', 'type', 'isPosted', 'messageBox', 'currentKey', 'prevKey', 'timeTaken']:
                    if target in value.keys(): 
                        info[target] = value[target]

                tmp = row.loc[['datumType', 'offsetTimestamp', 'timestamp', 'value']]
                tmp['offsetTimestamp'] = str(tmp['offsetTimestamp'])[:10] + 'T' + str(tmp['offsetTimestamp'])[11:] + '.000Z'
                tmp['timestamp'] = str(tmp['timestamp']) + ''
                tmp['pretty_value'] = info
                find_rows = find_rows.append(tmp)
                break
        
        if not find:
            id = get_unique_id(row)
            if id in df_dict.keys():
                df_dict[id] = (df_dict[id][0], df_dict[id][1] + 1)
            else:
                df_dict[id] = (0, 1)


    for idx, row in find_rows.iterrows():
        id = get_unique_id(row)
        df_dict[id] = (df_dict[id][0] + 1, df_dict[id][1])
        cnt, total_cnt = df_dict[id]

        find_rows.loc[idx, 'count'] = f'{cnt} / {total_cnt}'

    find_rows = find_rows[['offsetTimestamp', 'timestamp', 'pretty_value', 'datumType', 'count']]
    print(find_rows.to_string())
    find_rows.to_excel('result.xlsx', encoding='utf-8', float_format='%s')

if __name__ == '__main__':
    main()
