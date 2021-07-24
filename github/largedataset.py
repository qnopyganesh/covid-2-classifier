import Bio.SeqIO as bio
import pickle

datasetCnt = 10000
datasetFile = {'Alphacoronavirus': {'cnt': 0, 'fileId': 0, 'file': None},
               'Beata-MERS': {'cnt': 0, 'fileId': 0, 'file': None},
'Beata-SARS 2': {'cnt': 0, 'fileId': 0, 'file': None}}

def wrriteFile(className, x):
    if datasetFile[className]['cnt'] % datasetCnt == 0:
        if datasetFile[className]['file'] != None:
            datasetFile[className]['file'].close()
            datasetFile[className]['file'] = None
        datasetFile[className]["fileId"] = datasetFile[className]["fileId"] + datasetCnt
        datasetFile[className]['file'] = open(
            f'largedataset/{className}_{datasetFile[className]["fileId"] - datasetCnt}-{datasetFile[className]["fileId"]}.csv', 'w')
        datasetFile[className]['file'].writelines("id,genome,class")
    datasetFile[className]['file'].writelines(f'\n{x.id},{x.seq},{description}')


file = 'ncbi_dataset/data/genomic.fna'
# file = 'dataset/MERS/genomic.fna'
i = 0

file1 = open(file, 'r')
count = 0

while True:
    count += 1

    # Get next line from file
    line = file1.readline()

    # if line is empty
    # end of file is reached
    if not line:
        break
    if i == 10000:
        break
    i += 1
    # print("Line{}: {}".format(count, line.strip()))

file1.close()
i = 0



for x in bio.parse(file, 'fasta'):

    description = x.description[x.description.index(' '):x.description.rindex(',')].strip()
    description = description[0:description.rindex(' ')].strip()
    flag = 1
    try:
        if description.index('Human coronavirus') >= 0:
            description = 'Alphacoronavirus'
    except ValueError:
        try:
            if description.index("Severe acute respiratory syndrome coronavirus 2") >= 0:
                description = 'Beata-SARS 2'
        except ValueError:
            try:
                if description.index("Middle East respiratory syndrome") >= 0:
                    description = 'Beata-MERS'
            except ValueError:
                flag = 0
                print(description)
    if flag == 1:
        wrriteFile(description, x)
        datasetFile[description]['cnt'] = datasetFile[description]['cnt'] + 1
        print(f'{description}: {datasetFile[description]["cnt"]}')

for className in datasetFile:
    if datasetFile[className]['file'] != None:
        datasetFile[className]['file'].close()
# print(x.description)
# print(f'{i} : {description}')
