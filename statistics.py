'''
By: Jonah Stegman
Classifier for ENGG*6500 project
This file gives raw statistics of the data set
'''
import os
import pandas as pd


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

if __name__ == "__main__":
    path = os.path.dirname(__file__)
    input_file = "data/out3.csv"
    df = pd.read_csv(os.path.join(path, input_file))
    df['Country'].fillna('zz', inplace=True)
    country_stats(df)
    URL_breakdown(df)