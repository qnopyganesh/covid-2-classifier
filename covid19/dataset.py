import Bio.SeqIO as bio
import pickle


def buildDictKmers(sequence, ksize, dictnum, Dict, DictCnt):
    n = dictnum
    flag = 1
    for i in range(len(sequence) - ksize):
        kmer = sequence[i:i + ksize]
        if not Dict.get(kmer):
            Dict.update({kmer: n})
            DictCnt.update({kmer: 0})
            n = n + 1
        if flag == 1:
            DictCnt.update({kmer: DictCnt[kmer] + 1})
            flag = 0


def termToFrequencyKmers(sequence, ksize, Dict):
    frequencyTerm = [0] * len(Dict);
    for i in range(len(sequence) - ksize):
        kmer = sequence[i:i + ksize]
        if Dict.get(kmer):
            frequencyTerm[Dict.get(kmer) - 1] = frequencyTerm[Dict.get(kmer) - 1] + 1
    return frequencyTerm


def readDatasetFile(filename, records,outputs,value):
    for x in bio.parse(filename, 'fasta'):
        records.append(x.seq)
        outputs.append(value)


def readDataset():
    filename = "dataset/"
    records = []
    outputs = []
    for key in datasetFile:
        readDatasetFile(filename + key + '/genomic.fna', records,outputs,datasetFile[key])


    for i in range(9):
        kmerSize = i + 2
        freqRecords = []
        Dict = {}
        DictCnt = {}
        DictFilter = {}
        dictnum = 1
        print(f'Calcaulate freq : {kmerSize}')
        for x in range(len(records)):
            buildDictKmers(records[x], kmerSize, dictnum, Dict, DictCnt)
        dictnum = 1
        for key, value in DictCnt.items():
            if (value >= truncateMap):
                DictFilter.update({key: dictnum})
                dictnum = dictnum + 1

        for x in range(len(records)):
            freqRecords.append(termToFrequencyKmers(records[x], kmerSize, DictFilter))
        print(f'Dict Size : {len(DictFilter)}')
        with open(f'dataset/kemr-{kmerSize}-records.pickle', 'wb') as f:
            pickle.dump(freqRecords, f)
        with open(f'dataset/kemr-{kmerSize}-dict.pickle', 'wb') as f:
            pickle.dump(DictFilter, f)
    with open(f'dataset/output.pickle', 'wb') as f:
        pickle.dump(outputs, f)




truncateMap = 3
datasetFile = {'Alphacoronavirus': 1, 'MERS': 2}

#readDataset()

# readDataset(datasetFile, kmerSize, dictnum, Dict)
print('completed')
