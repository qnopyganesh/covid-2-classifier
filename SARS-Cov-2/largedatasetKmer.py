import Bio.SeqIO as bio
import pickle
import os
import pandas

truncateMap = 3

datasetFile = {'Alphacoronavirus': 1,
               'Beata-MERS': 2,
               'Beata-SARS 2': 3}
start_path = "largedataset/dataset"


def buildDictKmers(sequence, ksize, DictCnt):
    flag=1
    for i in range(len(sequence) - ksize):
        kmer = sequence[i:i + ksize]
        if not DictCnt.get(kmer):
            DictCnt.update({kmer: 0})
        if flag == 1:
            DictCnt.update({kmer: DictCnt[kmer] + 1})
            flag = 0


def termToFrequencyKmers(sequence, kmer, DictFilter):
    frequencyTerm = [0] * len(DictFilter);
    for i in range(len(sequence) - kmer):
        kmerStr = sequence[i:i + kmer]
        if DictFilter.get(kmerStr):
            frequencyTerm[DictFilter.get(kmerStr) - 1] = frequencyTerm[DictFilter.get(kmerStr) - 1] + 1
    return frequencyTerm


def readDatasetDict(kmer):
    DictCnt = {}
    DictFilter = {}
    basepath = 'largedataset/kmer/'
    for path, dirs, files in os.walk(start_path):
        for filename in files:
            print(os.path.join(path, filename))

            df = pandas.read_csv(os.path.join(path, filename))
            row_count, column_count = df.shape

            for i in range(row_count):
                buildDictKmers(df.iloc[i][1], kmer, DictCnt)
            print(f'Dict Size: {len(DictCnt)}')

        dictnum = 1
        print(f'Total Dict Size: {len(DictCnt)}')
        for key, value in DictCnt.items():
            if (value >= truncateMap):
                DictFilter.update({key: dictnum})
                dictnum = dictnum + 1

        print(f'filter Dict Size: {len(DictFilter)}')

    for path, dirs, files in os.walk(start_path):
        for filename in files:
            print(os.path.join(path, filename))
            df = pandas.read_csv(os.path.join(path, filename))
            row_count, column_count = df.shape
            freqRecords = []
            pathFile = basepath + filename

            outputs = []
            for i in range(row_count):
                freqRecords.append(termToFrequencyKmers(df.iloc[i][1],  kmer, DictFilter))
                outputs.append(datasetFile[df.iloc[i][2]])
            if not os.path.exists(pathFile):
                os.makedirs(pathFile)

            #obj = {'records': freqRecords, "output": outputs}

            with open(f'{pathFile}/kemr-{kmer}-records.pickle', 'wb') as f:
                pickle.dump(freqRecords, f)


    with open(f'{basepath}/dict-{kmer}.pickle', 'wb') as f:
        pickle.dump(DictFilter, f)


for i in range(2, 11):
    readDatasetDict(i)
