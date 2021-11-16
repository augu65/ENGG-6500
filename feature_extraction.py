'''
By: Jonah Stegman
feature extraction for ENGG*6500 project
This file extracts features from url csv's for evaluation
in a machine learning program
'''
import pandas as pd
import numpy as np
import os
import re

def protocol(df):
    '''
    Protocol:
     1 means http
     2 means https
     3 means ftp
     0 means none or other
    :param df:
    :return: df
    '''
    df['Protocol'] = 0
    df.loc[df['URL'].str.contains(r"^http:", case=False), 'Protocol'] = 1
    df.loc[df['URL'].str.contains(r"^https:", case=False), 'Protocol'] = 2
    df.loc[df['URL'].str.contains(r"^ftp:", case=False), 'Protocol'] = 3
    return df


def website(df):
    '''
    This holds the url value between the main website and the domain
    :param df:
    :return: df
    '''
    website = []
    domain = []
    for x in df['URL']:
        value = re.split("^http(s|)://",x.lower())[-1]
        value =value.replace('www.','').split('.', 1)[0]
        if not value.isdecimal():
            website.append(value)
            value = re.split("^http(s|)://", x.lower())[-1]
            value =value.replace('www.', '').split('.', 1)[1].split('/')[0]
            domain.append(value)
        else:
            value = re.split("^http(s|)://", x.lower())[-1]
            value = value.replace('www.', '').split('/')[0]
            website.append(value)
            domain.append('')
    df['Domain'] = domain
    df['Primary'] = website
    return df

def url_path(df):
    '''
    This gets the path given from a URL
    :param df:
    :return: df
    '''
    path = []
    for x in df['URL']:
        if '/' in x:
            path.append(x.split('/',1)[-1])
        else:
            path.append("")
    df['Path'] = path
    return df

path = os.path.dirname(__file__)
input_file = "out.csv"
df = pd.read_csv(os.path.join(path, input_file))
df.loc[df['Label'].str.contains('benign'), 'Label'] = 0
df.loc[~df['Label'].str.contains('benign', na=True), 'Label'] = 1
df = protocol(df)
df = website(df)
df = url_path(df)

a = 1