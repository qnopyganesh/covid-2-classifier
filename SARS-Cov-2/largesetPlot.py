import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def plotGraph(TestSet):

    KMER = []
    Accuercy = []
    Time = []
    DictCnt = csv.iloc[0][5];

    for i in range(row_count):
        if (csv.iloc[i][1] == TestSet):
            KMER.append(csv.iloc[i][0])
            Accuercy.append(csv.iloc[i][2])
            Time.append(csv.iloc[i][3])

    data = {'KMER': KMER, 'Accuercy': Accuercy, 'Time': Time}
    # convert dictionary to a dataframe
    df = pd.DataFrame(data)
    # Print out all rows
    print(df[:])

    matplotlib.rc_file_defaults()
    ax1 = sns.set_style(style=None, rc=None)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel('K-MER', fontsize=16)
    ax1.set_title(f'Data Set : {TestSet}', fontsize=16)
    ax1.set_ylabel('Time in milliseconds', fontsize=16)
    sns.lineplot(data=df['Time'], marker='o', sort=False, ax=ax1)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Accuercy in %', fontsize=16)
    sns.barplot(data=df, x='KMER', y='Accuercy', alpha=0.5, ax=ax2)

    plt.show()
    print(df[:])


csv = pd.read_csv('largedataset/resultFinal.csv')
row_count, column_count = csv.shape

for i in range(10):
    plotGraph(csv.iloc[i][1])
