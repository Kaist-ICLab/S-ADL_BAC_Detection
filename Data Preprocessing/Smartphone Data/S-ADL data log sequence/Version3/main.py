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

    req_idx = 0
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

    for idx, row in df.iterrows():
        if str(row[finish_time_idx]) > str(finish_time):
            break

        # Find init time
        if req_idx == 0:
            if str(row[prev_time_idx]) >= str(prev_time):
                prev_time = init_time
            else:
                continue

        for req in reqs[2:]:
            # Find specified event
            req = req.split('-')
            find = False

            if row['datumType'] == req[0]:
                if len(req) == 1:
                    find = True
                else:
                    value = json.loads(row['value'])
                    if ('type' in value.keys() and value['type'] == req[1]) or\
                    ('packageName' in value.keys() and value['packageName'] == req[1]) or\
                    ('isPosted' in value.keys() and value['isPosted'] == req[1]) or\
                    ('messageBox' in value.keys() and value['messageBox'] == req[1]):
                        if len(req) == 2:    
                            find = True
                        elif ('type' in value.keys() and value['type'] == req[2]) or\
                        ('isPosted' in value.keys() and str(value['isPosted']) == req[2]):
                            find = True

            if find:
                info = dict()
                for target in ['type', 'packageName', 'isPosted', 'messageBox']:
                    if target in value.keys(): 
                        info[target] = value[target]
                
                info = pd.DataFrame([[info]])
                tmp = row.loc[['datumType', 'offsetTimestamp', 'timestamp']]
                tmp['value'] = info[0][0]
                find_rows = find_rows.append(tmp)
                break

    print(find_rows)
    find_rows.to_csv('result.csv')

if __name__ == '__main__':
    main()