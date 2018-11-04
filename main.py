import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
import pickle

from internet_data.fetch_data import *
from analysis.analysis import *



# fetch_data.download("data.pickle")

data = fetch_data.load("data.pickle" ,"2018-01-01" ,"2018-12-31")

analysiser = analysis(data)

index ,value = analysiser.get_date("raw")
print(pd.DataFrame(value ,index=index))

plt.figure(1)
plt.bar(index ,value)
plt.show()

