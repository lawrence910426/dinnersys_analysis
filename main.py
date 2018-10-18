from fetch_data import *
from data_structure.order import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

fetcher = fetch_data("dinnersys", "2rjurrru")

data = get_order(fetcher, "2018/10/17-00:00:00", "2018/10/19-00:00:00")
dish = get_dish(fetcher)

datecount = {}
for key in data:
    date = data[key].date
    date = date.split(" ")[0]
    did = data[key].dish.id

    if datecount.setdefault(date) is None:
        datecount[date] = {}
        datecount[date]["summa"] = 0
    if datecount[date].setdefault(did) is None:
        datecount[date][did] = 0
    datecount[date][did] += 1
    datecount[date]["summa"] += 1

transfer = np.zeros((len(dish), len(dish)) ,dtype=np.float64)

for bkey in dish:
    before = dish[bkey]
    for akey in dish:
        after = dish[akey]

        if datecount["2018-10-18"]["summa"] == 0: # or datecount["2018-10-17"]["summa"] == 0:
            continue
        if datecount["2018-10-18"].setdefault(after.id) is None: # or datecount["2018-10-17"].setdefault(before.id) is None:
            continue
        
        # before_p = datecount["2018-10-17"][before.id] / datecount["2018-10-17"]["summa"]
        after_p = datecount["2018-10-18"][after.id] / datecount["2018-10-18"]["summa"]    
        transfer[int(bkey) - 1, int(akey) - 1] = after_p
        
        # print(before_p ,after_p ,before_p * after_p ,transfer[int(bkey) ,int(akey)] ,bkey ,akey)
        # os.system("pause")

for bkey in dish:
    sum = 0
    for akey in dish:
        sum += transfer[int(bkey) - 1][int(akey) - 1]
        print(transfer[int(bkey) - 1][int(akey) - 1])
    print(sum)
    os.system("pause")
    