'''
By: Jonah Stegman
Classifier for ENGG*6500 project
This file gives raw statistics of the data set
'''
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def country_stats(df):
    print('US: ' + str(sum(df['Country'].str.contains('US'))))
    print('Veitnam: ' + str(sum(df['Country'].str.contains('VN'))))
    print('China: ' + str(sum(df['Country'].str.contains('CN'))))
    print('US Benign: ' + str(sum((df['Country'].str.contains('US')) & (df['Label'].str.contains('benign')))))
    print('Veitnam Benign: ' + str(sum((df['Country'].str.contains('VN')) & (df['Label'].str.contains('benign')))))
    print('China Benign: ' + str(sum((df['Country'].str.contains('CN')) & (df['Label'].str.contains('benign')))))
    print('all Benign: ' + str(sum((df['Country'].str.contains('CN|US|VN')))))
    print('all Benign: ' + str(sum((df['Country'].str.contains('CN|US|VN')) & (df['Label'].str.contains('benign')))))

def URL_breakdown(df):
    benign = sum(df['Label'].str.contains('benign'))
    malicious = sum(~df['Label'].str.contains('benign'))
    total = df['Label'].count()
    print(f"benign: {str(benign)}, malicious: {str(malicious)}, Total: {str(total)}")
    benignP = benign/total
    malP = malicious/total
    print(f"% of benign: {str(benignP)}")
    print(f"% of maalicious: {str(malP)}")


def false_positive(path):
    data = "data/extracted_features2.csv"
    fp = "data/fp.csv"
    df = pd.read_csv(os.path.join(path, data))
    df2 = pd.read_csv(os.path.join(path, fp))
    df2['URL'] = ''
    for x in range(len(df2['index'])):
        df2['URL'][x] = df['URL'][df2['index'][x]]
    boxplot = df2.boxplot(column=['Domain','Num_Symbol'])
    plt.ylim(0, 100)
    plt.xlabel('Feature')
    plt.ylabel('Value')
    plt.title('Visualize FP Dataframe')
    plt.show()
    a=1

def false_negatives(path):
    data = "data/extracted_features2.csv"
    fp = "data/fn.csv"
    df = pd.read_csv(os.path.join(path, data))
    df2 = pd.read_csv(os.path.join(path, fp))
    df2['URL'] = ''
    for x in range(len(df2['index'])):
        df2['URL'][x] = df['URL'][df2['index'][x]]

    x = [range(len(df2['URL']))]
    x = np.array(x).reshape(len(df2['URL']))
    print(df2['rank'].mean())
    boxplot = df2.boxplot(column=['Path'])
    plt.xlabel('Feature')
    plt.ylabel('Value')
    plt.title('Visualize FN Dataframe')
    plt.show()
    a=1

if __name__ == "__main__":
    path = os.path.dirname(__file__)
    # input_file = "data/out3.csv"
    # df = pd.read_csv(os.path.join(path, input_file))
    # df['Country'].fillna('zz', inplace=True)
    # country_stats(df)
    # URL_breakdown(df)
    false_positive(path)
    #false_negatives(path)