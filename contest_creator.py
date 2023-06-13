from collections import defaultdict
import requests
import csv
from datetime import datetime, timedelta
from local import TOKEN

# hyper paramter
lim = 11

# 基準となるスケジュール
target_csv = 'schedule.csv'
p_set = defaultdict(list)
with open(target_csv, mode='r', encoding='utf-8-sig') as f:
    problems = csv.DictReader(f)
    for p in problems:
        y, m, d = map(int, p['date'].split('-'))
        date = datetime(y, m, d, 7, 30)
        # print(date)
        p_set[date].append(p['ID'])

# 開始日を決定
y = datetime.now().year
print(f'current year is {y}')
print('enter starting MONTH DATE ex)1 1,12 25 etc')
m, d = map(int, input().split(' '))
start = datetime(y, m, d, 7, 30)
print(f'starting date is {start}, okay? y')
if input() != 'y':
    exit(0)
cnt = 0

# 作成日数を決定

print(f'enter the number of creating contest')
lim = int(input())
print(f'the number is {lim}')
end = start + timedelta(days=lim - 1)
print(f'end date is {end}, okay? y')
if input() != 'y':
    exit(0)


for date, problems in p_set.items():
    if date < start:
        continue
    if cnt == lim:
        break
    print(date)
    print(problems)
    problem_query = []

    for i, p in enumerate(problems):
        problem_query.append({'id': p, 'point': 1, "order": i+1})

    m = date.month
    d = date.day
    title = f'あさかつ{m}/{d}'
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'token=' + TOKEN,
    }
    timestamp = int(datetime.timestamp(date))

    res = requests.post('https://kenkoooo.com/atcoder/internal-api/contest/create', headers=headers, json={
        'title': title,
        'memo': '難易度は灰灰茶緑水青（含：試験管）です。感想戦などは https://discord.gg/6JbTEBnfrY でやっています。',
        'start_epoch_second': int(timestamp),
        'duration_second': 3600,
        'mode': None,
        'is_public': True,
        'penalty_second': 300,
    })

    if res.status_code != 200:
        print('contest creation failed!')
        exit(0)

    contest_id = res.json()['contest_id']
    contest_url = 'https://kenkoooo.com/atcoder/#/contest/show/' + contest_id
    print('contest created : https://kenkoooo.com/atcoder/#/contest/show/' + contest_id)

    res = requests.post('https://kenkoooo.com/atcoder/internal-api/contest/item/update', headers=headers, json={
        'contest_id': contest_id,
        'problems': problem_query,
    })

    with open('announce.txt', mode='a', encoding='utf-8') as f:
        f.write(f'{title}\n{contest_url}\n')

    cnt += 1