'''
By: Jonah Stegman
feature extraction for ENGG*6500 project
This file extracts features from url csv's for evaluation
in a machine learning program
'''
import pandas as pd
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
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
            website.append(len(value))
            value = re.split("^http(s|)://", x.lower())[-1]
            value =value.replace('www.', '').split('.', 1)[-1].split('/')[0]
            domain.append(len(value))
        else:
            value = re.split("^http(s|)://", x.lower())[-1]
            value = value.replace('www.', '').split('/')[0]
            website.append(len(value))
            domain.append(0)
    df['Domain'] = domain
    df['Primary'] = website
    return df

def url_path(df):
    '''
    This gets the length of the path given from a URL
    and the number of directories
    :param df:
    :return: df
    '''
    path = []
    num_path = []
    for x in df['URL']:
        if '/' in x:
            x = x.split('/', 1)
            path.append(len(x[-1]))
            x = x[-1].split('/')
            num_path.append(len(x))
        else:
            path.append(0)
            num_path.append(0)
    df['Path'] = path
    df['Num_Paths'] = num_path
    return df

def num_characters(df):
    '''
    Gets the number of digits in the url
    Gets the number of alpha characters in the url
    Gets the number of symbols in the url
    :param df:
    :return: df
    '''
    digits = []
    alpha = []
    symbol = []
    for x in df['URL']:
        sumd = sum(c.isdigit() for c in x)
        suma = sum(c.isalpha() for c in x)
        digits.append(sumd)
        alpha.append(suma)
        symbol.append(len(x)-sumd-suma)
    df['Num_Digits'] = digits
    df['Num_Alpha'] = alpha
    df['Num_Symbol'] = symbol
    return df


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    input_file = "data/out3.csv"
    df = pd.read_csv(os.path.join(path, input_file))
    df['Country'].fillna('zz', inplace=True)
    df = df.drop('URL2', 1)
    df.loc[df['Label'].str.contains('benign'), 'Label'] = 0
    df.loc[~df['Label'].str.contains('benign', na=True), 'Label'] = 1
    df = protocol(df)
    df = website(df)
    df = url_path(df)
    df = num_characters(df)
    df.to_csv('extracted_features.csv',index=False)
    a = 1