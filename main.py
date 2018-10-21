import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
from internet_data.fetch_data import *
from analysis.transfer_matrix import *
import pandas as pd


fetcher = fetch_data("dinnersys", "2rjurrru")
data = get_order(fetcher, "2018/10/17-00:00:00", "2018/10/19-00:00:00")
matrix = transfer_matrix(data)
m = matrix.get_matrix("2018/09/01" ,"2018/10/19")

opt = np.zeros(m.shape ,dtype=np.float64)
raw = np.zeros((m.shape[0] ,1) ,dtype=np.float64)
raw[0 ,0] = 1

for i in range(m.shape[0]):
    summa = 0
    for j in range(m.shape[1]):
        summa += m[i ,j]
    if(summa == 0):
        continue
    for j in range(m.shape[1]):
        opt[j ,i] = m[i ,j] / summa

for i in range(100):
    raw = opt.dot(raw)

print(pd.DataFrame(raw))
