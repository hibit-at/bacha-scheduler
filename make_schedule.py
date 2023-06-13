import csv
from random import sample
import requests
from datetime import datetime, timedelta
from collections import defaultdict


# スケジュールをつぎたすCSVのパス

# target_csv = 'sample.csv'
target_csv = 'schedule.csv'

# 作成開始する日
pasts = csv.DictReader(open(target_csv, mode='r', encoding='utf-8-sig'))
list_pasts = list(pasts)
last_date = list_pasts[-1]['date']
year, month, day = map(int, last_date.split('-'))
day_count = datetime(year=year, month=month, day=day) + timedelta(days=1)
print(day_count)

# 作成する日数
create_days = 10

check = defaultdict(bool)
pasts = csv.DictReader(open(target_csv, mode='r', encoding='utf-8-sig'))
for past in pasts:
    ID = past['ID']
    year, month, day = map(int, past['date'].split('-'))
    date = datetime(year=year, month=month, day=day)
    criteria = day_count - timedelta(days=60)
    if date >= criteria:
        check[ID] = True
url = 'https://kenkoooo.com/atcoder/resources/problem-models.json'
problems = requests.get(url).json()
problems_by_level = defaultdict(list)
borders = [50, 400, 800, 1200, 1600, 2000, 1e18]


def diff_calc(diff):
    for i, border in enumerate(borders):
        if diff < border:
            return i


for ID, content in problems.items():
    if check[ID]:
        continue
    if not 'difficulty' in content:
        continue
    diff = content['difficulty']
    problems_by_level[diff_calc(diff)].append(ID)


while create_days:
    year = day_count.year
    month = day_count.month
    day = day_count.day
    date_str = '-'.join(map(str, [year, month, day]))
    print(date_str)
    for i in range(6):
        problem_list = problems_by_level[i]
        pick = sample(problem_list, 1)[0]
        problem_list.remove(pick)
        print(pick)
        with open(target_csv, mode='a', newline='') as f:
            csv.writer(f).writerow([pick, date_str])
    day_count += timedelta(days=1)
    create_days -= 1
