import random
import csv

with open('./tests/dataset.csv', 'a') as f:
    for i in range(100):
        n1: float = random.uniform(0, 2 << 15)
        n2: float = random.uniform(0, 2 << 15)
        w = csv.writer(f)
        w.writerow((n1, n2))
