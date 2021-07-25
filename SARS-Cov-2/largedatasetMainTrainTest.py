from sklearn.preprocessing import MinMaxScaler
from train import *
from validate import *
import pickle
import os

Dict = {}
dictnum = 1
noOfUnits = 10
dropout = 0.2
noOFClass = 3
epochs = 10
batchSize = 64


# maxGenomes = 27000

def readPincleFile(filename):
    recordsInt = []
    with open(filename, 'rb') as f:
        recordsInt = pickle.load(f)
        return recordsInt


def getOutputArray(classLabel):
    if classLabel == 1:
        return [1, 0, 0]
    elif classLabel == 2:
        return [0, 1, 0]
    else:
        return [0, 0, 1]


def readPickleFile(recordsFile, records, outputs, recordsFileClass):
    recordsInternal = readPincleFile(recordsFile)
    records += recordsInternal
    output = getOutputArray(recordsFileClass)
    for j in range(len(recordsInternal)):
        outputs.append(output)


def divdeDatsset(training_set_scaled, outputs, records):
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    for i in range(len(records)):
        if i % 2 == 0 and i <= 10000:
            x_train.append(training_set_scaled[i, :])
            y_train.append(outputs[i])
        else:
            x_test.append(training_set_scaled[i, :])
            y_test.append(outputs[i])

    return x_train, y_train, x_test, y_test


def validate(x_test, y_test):
    x_test, y_test = np.array(x_test), np.array(y_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = np.reshape(y_test, (y_test.shape[0], y_test.shape[1], 1))
    score = regressor.evaluate(x_test, y_test, verbose=0)
    return score


def printScore(scores, regressor):
    print(scores)
    for i in range(len(regressor.metrics_names)):
        print("%s: %.2f%%" % (regressor.metrics_names[i], scores[i] * 100))


def termToFrequencyKmers(sequence, kmer, DictFilter):
    frequencyTerm = [0] * len(DictFilter);
    for i in range(len(sequence) - kmer):
        kmerStr = sequence[i:i + kmer]
        if DictFilter.get(kmerStr):
            frequencyTerm[DictFilter.get(kmerStr) - 1] = frequencyTerm[DictFilter.get(kmerStr) - 1] + 1
    return frequencyTerm


def validateTest(x_test, regressor):
    # Part 3 - Making the predictions and visualising the results
    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predicted_output = regressor.predict(x_test)
    return predicted_output


k = 8
filename = f'largedataset/model/{k}-model.h5'

from keras.models import Sequential

# Initialising the RNN
regressor = Sequential()
Dict = readPincleFile(f'largedataset\kmer\dict-{k}.pickle')

print(f'Dictionory Size:  {len(Dict)}')

datasetCSV = open(
    f'largedataset/result.csv',
    'w')
datasetCSV.writelines("k-mer,Test set,accuracy,Time,Loss,Dict Size")

recordsFile = [f'largedataset\kmer\Alphacoronavirus_0-10000.csv\kemr-{k}-records.pickle',
               f'largedataset\kmer\Beata-MERS_0-10000.csv\kemr-{k}-records.pickle',
               f'largedataset\kmer\Beata-SARS 2_0-10000.csv\kemr-{k}-records.pickle']
recordsFileClass = [1,
                    2,
                    3]

records = []
outputs = []
for i in range(len(recordsFile)):
    readPickleFile(recordsFile[i], records, outputs, recordsFileClass[i])

sc = MinMaxScaler(feature_range=(0, 1))

training_set_scaled = sc.fit_transform(records)

x_train, y_train, x_test, y_test = divdeDatsset(training_set_scaled, outputs, records)

train(x_train, y_train, regressor, noOfUnits, dropout, noOFClass, epochs, batchSize)

scores = validate(x_test, y_test)

printScore(scores, regressor)
