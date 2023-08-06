'''
Description: this file contains helpers relevant for automated machine learning


'''

from copy import copy

import numpy as np
from numpy import inf
import pandas as pd
from datetime import datetime
import functools
import matplotlib.pyplot as plt  

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier  #RF and GBM algorithm
from sklearn.linear_model import ElasticNet, SGDClassifier, LogisticRegression
from sklearn.model_selection import GridSearchCV   #Perforing grid search
from sklearn import preprocessing, neighbors, metrics, svm
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.metrics import mean_absolute_error, accuracy_score, log_loss, make_scorer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils.multiclass import unique_labels

import sklearn
if sklearn.__version__<'0.20':
    from sklearn.cross_validation import train_test_split, KFold, StratifiedKFold, PredefinedSplit
else:
    from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, PredefinedSplit


def create_feature_metadata(this_df,outfile='feature_types.csv'):
    """
    Creates categorization of features as Numeric, Categorical, and Text and saves it in the .csv
    Returns: dataframe with feature information
    """
    data_len=len(this_df)

    df_describe=this_df.describe(include = 'all',datetime_is_numeric=False).T.reset_index().rename(columns={'index':'feature_name'})
    df_unique = pd.DataFrame([[col,this_df[col].nunique()] for col in this_df.columns],columns=['feature_name','num_unique'])

    
    df_describe = df_describe.merge(df_unique,how='left',on=['feature_name'])
    df_describe['feature_type']=''
    df_describe.loc[np.logical_and(df_describe['mean'].notnull(),df_describe['num_unique']>min(.05*data_len,100)),'feature_type']='Numeric'
    df_describe.loc[np.logical_and(df_describe['mean'].isnull(),df_describe['num_unique']<.05*data_len),'feature_type']='Categorical'
    df_describe.loc[np.logical_and(df_describe['mean'].isnull(),df_describe['num_unique']>=.05*data_len),'feature_type']='Text'
    
    missing_counts=this_df.isnull().sum()
    missing_counts=pd.DataFrame({"feature_name":missing_counts.index,"missing_count":missing_counts.values})
    df_describe=df_describe.merge(missing_counts,how='left',on=['feature_name'])

    df_describe.to_csv(outfile,index=False)
    return df_describe
