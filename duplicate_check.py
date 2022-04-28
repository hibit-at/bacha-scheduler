import csv
from random import sample
import requests
from datetime import datetime, timedelta
from collections import defaultdict

target_csv = 'schedule.csv'

check = defaultdict(list)
pasts = csv.DictReader(open(target_csv, mode='r', encoding='utf-8-sig'))
for past in pasts:
    ID = past['ID']
    date = past['date']
    check[ID].append(date)

check = sorted(check.items(), key=lambda x : len(x[1]))

for c in check:
    print(c)