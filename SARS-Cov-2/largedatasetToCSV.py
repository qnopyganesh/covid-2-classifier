import Bio.SeqIO as bio
import pickle
import os
import pandas
import glob
import csv
import pandas as pd
import numpy as np


def readPincleFile(filename):
    recordsInt = []
    with open(filename, 'rb') as f:
        recordsInt = pickle.load(f)
        return recordsInt


start_path = "largedataset/kmer"

# root_dir needs a trailing slash (i.e. /root/dir/)
for filename in glob.iglob(start_path + '**/**/*.pickle', recursive=True):
    print(filename)
    data = readPincleFile(filename)
    filename = filename.replace(".pickle", ".csv")
    try:
        if filename.index("dict") >= 0:
            with open(filename, 'w') as f:
                for key in data.keys():
                    f.writelines(f'{key},{data[key]}\n')
                f.close()
    except ValueError:
        DF = pd.DataFrame(data)
        # save the dataframe as a csv file
        DF.to_csv(filename)
#print(data)
