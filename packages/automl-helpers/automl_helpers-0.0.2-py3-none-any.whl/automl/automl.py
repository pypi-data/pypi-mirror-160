'''
Description: this file contains classes relevant for automated machine learning
Classes: MissingDataHandler, TextElasticNetBinary, TextElasticNetRegression, StackLayer


'''

from copy import copy

import itertools
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

#import scipy.stats as st

#missing data handler
class MissingDataHandler(BaseEstimator, TransformerMixin):
    def __init__(self,method='large_value', columns=None, imputation_funcs=None,imputation_values=None,create_dummy=False):
        self.method=method        
        self.columns=columns
        self.create_dummy=create_dummy
        self.imputation_funcs=imputation_funcs
        self.imputation_values=imputation_values
        if self.columns==None:
            self.columns=[]
        if self.imputation_funcs==None:
            self.imputation_funcs=[]
        if self.imputation_values==None:
            self.imputation_values=[]

        self.feature_names_out=self.columns.copy()

    def get_feature_names_out(self, input_features=None):
        return self.feature_names_out

    def fit(self,X,y=None,columns=None):
        if not self.columns:
            self.columns=list(X.columns)
        elif columns:
            self.columns=columns
        self.feature_names_out=self.columns.copy()
            
        self.imputation_values=np.zeros(len(self.columns))
        self.has_missing=np.zeros(len(self.columns), dtype=bool)
        for i in range(len(self.columns)):
            feat=self.columns[i]
            if self.method=='large_value':
                self.imputation_values[i]=-1*(10**int(np.log10(np.max(np.abs(X[feat]),axis=0))+2)-1)
            if self.method=='median':
                self.imputation_values[i]=np.nanmedian(X[feat])
            if np.sum(X[feat].isnull())>0:
                self.has_missing[i]=True
                if self.create_dummy:
                    self.feature_names_out.append(feat+'_#mi')

    def fit_transform(self,X,y=None,columns=None):
        X=X.copy()
        if not self.columns and not columns:
            self.columns=list(X.columns)
        elif columns:
            self.columns=columns
        self.feature_names_out=self.columns.copy()

        self.imputation_values=np.zeros(len(self.columns))
        self.has_missing=np.zeros(len(self.columns), dtype=bool)
        for i in range(len(self.columns)):
            feat=self.columns[i]
            if self.method=='large_value':
                self.imputation_values[i]=-1*(10**int(np.log10(np.max(np.abs(X[feat]),axis=0))+2)-1)
            if self.method=='median':
                self.imputation_values[i]=np.nanmedian(X[feat])
            
            feat=self.columns[i]
            #only create dummy and imputation value if training set has missing
            if np.sum(X[feat].isnull())>0:
                self.has_missing[i]=True
                if self.create_dummy:
                    X[feat+'_#mi']=1*X[feat].isnull()
                    self.feature_names_out.append(feat+'_#mi')

            X.loc[X[feat].isnull(),feat]=self.imputation_values[i]
        return X

    def transform(self,X,y=None):
        X=X.copy()
        for i in range(len(self.columns)):
            feat=self.columns[i]
            if self.has_missing[i] and self.create_dummy:
                X[feat+'_#mi']=1*X[feat].isnull()
            X.loc[X[feat].isnull(),feat]=self.imputation_values[i] 
                 
        return X

#Model to directly fit logistic regression on a test data field
class TextElasticNetBinary(BaseEstimator, ClassifierMixin):
    def __init__(self,max_words=10000,min_occurrence=10,text_preprocessor=None, token_pattern=None, penalty_C=.5,l1_ratio=.5,ngram_range=(1, 1)):
        self.max_words=max_words #max number of words in dictionary
        self.min_occurrence=min_occurrence #require number of observations word appears in
        self.text_preprocessor=text_preprocessor
        self.penalty_C=penalty_C
        self.l1_ratio=l1_ratio
        self.token_pattern=token_pattern
        self.ngram_range=ngram_range
        if self.token_pattern==None:
            self.tfidf=TfidfVectorizer(max_features=self.max_words,min_df=self.min_occurrence,ngram_range=self.ngram_range)
        else:
            self.tfidf=TfidfVectorizer(max_features=self.max_words,min_df=self.min_occurrence,token_pattern=self.token_pattern,ngram_range=self.ngram_range)
        self.enet=LogisticRegression(penalty='l1', tol=0.00001,C=penalty_C,solver='saga',max_iter=500)
        
    def fit(self,X,y):
        #train / test split to find Elastic Net
        if type(X)==pd.core.frame.DataFrame:
            X_series=pd.Series(X.iloc[:,0]).astype(str)
        else:
            X_series=pd.Series(X).astype(str)
        
        self.classes_ = unique_labels(y)

        #fit the tfidf
        text_features = pd.DataFrame(self.tfidf.fit_transform(X_series).toarray())
        #fit the elastic net model
        self.enet.fit(text_features,y)

    def predict(self,X):
        if type(X)==pd.core.frame.DataFrame:
            X_series=pd.Series(X.iloc[:,0]).astype(str)
        else:
            X_series=pd.Series(X).astype(str)
        text_features=pd.DataFrame(self.tfidf.transform(X_series).toarray())
        return self.enet.predict(text_features)

    def predict_proba(self,X):
        if type(X)==pd.core.frame.DataFrame:
            X_series=pd.Series(X.iloc[:,0]).astype(str)
        else:
            X_series=pd.Series(X).astype(str)
        text_features=pd.DataFrame(self.tfidf.transform(X_series).toarray())
        return self.enet.predict_proba(text_features)

    def predict_log_proba(self,X):
        if type(X)==pd.core.frame.DataFrame:
            X_series=pd.Series(X.iloc[:,0]).astype(str)
        else:
            X_series=pd.Series(X).astype(str)
        text_features=pd.DataFrame(self.tfidf.transform(X_series).toarray())
        return self.enet.predict_log_proba(text_features)

class TextElasticNetRegression(BaseEstimator):
    def __init__(self,max_words=10000,min_occurrence=10,text_preprocessor=None, token_pattern=None, alpha=1,l1_ratio=.5,ngram_range=(1,1)):
        self.max_words=max_words #max number of words in dictionary
        self.min_occurrence=min_occurrence #require number of observations word appears in
        self.text_preprocessor=text_preprocessor
        self.alph=alpha
        self.l1_ratio=l1_ratio
        self.token_pattern=token_pattern
        self.ngram_range=ngram_range
        if self.token_pattern==None:
            self.tfidf=TfidfVectorizer(max_features=self.max_words,min_df=self.min_occurrence,ngram_range=self.ngram_range)
        else:
            self.tfidf=TfidfVectorizer(max_features=self.max_words,min_df=self.min_occurrence,token_pattern=self.token_pattern,ngram_range=self.ngram_range)
        self.enet=ElasticNet(alpha=alpha,l1_ratio=l1_ratio)
        
    def fit(self,X,y):
        #train / test split to find Elastic Net
        if type(X)==pd.core.frame.DataFrame:
            X_series=pd.Series(X.iloc[:,0]).astype(str)
        else:
            X_series=pd.Series(X).astype(str)

        #fit the tfidf
        text_features = pd.DataFrame(self.tfidf.fit_transform(X_series).toarray())
        #fit the elastic net model
        self.enet.fit(text_features,y)

    def predict(self,X):
        if type(X)==pd.core.frame.DataFrame:
            X_series=pd.Series(X.iloc[:,0]).astype(str)
        else:
            X_series=pd.Series(X).astype(str)
        text_features=pd.DataFrame(self.tfidf.transform(X_series).toarray())
        return self.enet.predict(text_features) 


class StackLayer(BaseEstimator, TransformerMixin):
    def __init__(self, models, feature_lists=None, hyperparamater_lists=None,gridsearch_lists=None,regression=False,autotune=False,suffix="",verbose=0):
        """
        Description: Class to create a stack predictions on a single layer for use in larger model
        Details: Purpose is to be able to store a list of models and corresponidng hyperparameters, get out-of-fold predictions, 
            fit on full training data and save fitted model list, find best hyperparameters, manually set hyperparameters, ...
        Note: When using as part of Pipeline only use one model at a time instead of a list as multiple feature lists are not permitted.
        Next steps: consider making binary vs regression part of class, hyperparameters (?), add predict_proba of not regression 
        """
        self.verbose=verbose
        if self.verbose > 0:
            print("Initialize StackLayer ...")
        if self.verbose > 1:
            print(models)
        #list of models
        self.models=models 
        self.regression=regression        
        
        #feature list for each model (should be length 1 or # of models)
        self.feature_lists=feature_lists
        self.autotune=autotune
        self.suffix=suffix
        
        #to set manually instead of performing grid search or using defaults
        self.hyperparamater_lists=None
        if hyperparamater_lists!=None and len(models)==len(hyperparamater_lists):
            self.hyperparamater_lists=hyperparamater_lists
        elif hyperparamater_lists!=None:
            print("Unexpected error: length of hyperpameters list "+str(len(hyperparamater_lists))+" not equal to number of models "+ str(len(models)))
            raise
        
        #should be length # of models
        
        if gridsearch_lists!=None and len(models)==len(gridsearch_lists):
            self.gridsearch_lists=gridsearch_lists
        elif gridsearch_lists==None:
            self.gridsearch_lists=[]
        else:
            print("Unexpected error: length of gridsearch list "+str(len(gridsearch_lists))+" not equal to number of models "+ str(len(models)))
            raise
         
        #if one feature list just save that as outputs as either StackLayer+suffix or origianl feature name, else concatenate and do the same for each list
        if type(self.feature_lists[0])!=list:
            if len(self.feature_lists)>1:
                self.feature_names_out=["StackLayer"+self.suffix]
            else:
                self.feature_names_out=[self.feature_lists[0]+self.suffix]
        else:
            self.feature_names_out=[]
            for fff in range(len(self.feature_lists)):
                if len(self.feature_lists[fff])>1:
                    self.feature_names_out.append("StackLayer"+str(fff)+self.suffix)
                else:
                    self.feature_names_out.append(self.feature_lists[fff]+self.suffix)

    def get_feature_names_out(self, input_features=None):
        return self.feature_names_out

    #set hyperparmeter manually   
    def set_hyperparameters(self, hyperparamater_lists):        
        if hyperparamater_lists!=None and len(self.models)==len(hyperparamater_lists):
            self.hyperparamater_lists=hyperparamater_lists
        elif hyperparamater_lists!=None:
            print("Unexpected error: length of hyperpameters list "+str(len(hyperparamater_lists))+" not equal to number of models "+ str(len(models)))
            raise
    
    #TO BE UPDATED .. maybe this just grabs the hyperparameters from the model
    def get_hyperparameters(self):        
        return self.hyperparamater_lists
 
    #tune hyperparameters
    def tune_hyperparameters(self, X_train, y_train, gridsearch_lists=None, metric=None, n_jobs=4, cv=5, random_state=0):
        if self.verbose > 0:
            print("Inside tune_hyperparameters of StackLayer")
        
        #if passed in a gridsearch - otherwise use the one initiated previosly
        if gridsearch_lists==None:
            gridsearch_lists=self.gridsearch_lists
        if len(self.models)!=len(gridsearch_lists):
            print("Unexpected error: length of gridsearch list "+str(len(gridsearch_lists))+" not equal to number of models "+ str(len(models)))
            raise
            
        # Specify default metric for cross-validation
        if metric is None and self.regression:
            metric = make_scorer(mean_absolute_error, greater_is_better=False)
        elif metric is None and not self.regression:
            metric = make_scorer(log_loss, greater_is_better=False, needs_proba=True)      

        self.gridsearch_results=[]
        for mm in range(len(self.models)):
            gsearch = GridSearchCV(estimator = self.models[mm],param_grid = gridsearch_lists[mm], scoring=metric,n_jobs=n_jobs,cv=cv,refit=True)
            if len(self.feature_lists)==1:
                X_temp=X_train[self.feature_lists[0]]
            elif len(self.feature_lists)==len(self.models):
                X_temp=X_train[self.feature_lists[mm]]
            gsearch.fit(X_temp,y_train)
            gsearch.set_params()
            #save the best estimator from cv that was then fit on all the data
            self.models[mm]=gsearch.best_estimator_
            self.gridsearch_results.append(gsearch)
            if self.verbose>0:
                print(self.models[mm])  
                #print(gsearch.grid_scores_)
                print(gsearch.best_params_)
                print(gsearch.best_score_)

    # get out of fold predictions
    def get_oof_predictions(self, X_train, y_train, cv=5):
        # Print list of models
        if self.verbose > 1:
            print("List of models in Stack Layer: ")
            for mm in range(len(self.models)):
                print(self.models[mm])
        # If cv method not provided split indices to get folds
        if type(cv)==int:
            #split the data into 5 time cross validation folds
            cv = PredefinedSplit(test_fold=np.floor(cv*np.arange(len(X_train))/len(X_train)))

        if self.gridsearch_lists and self.autotune:
            self.tune_hyperparameters(X_train, y_train, cv=cv)
            
        oof_predictions=[]
        list_of_folds=cv.unique_folds
        for f in list_of_folds:
            X_train_fold=X_train.iloc[cv.test_fold!=f]
            X_test_fold=X_train.iloc[cv.test_fold==f]
            y_train_fold=y_train.iloc[cv.test_fold!=f]
            y_test_fold=y_train.iloc[cv.test_fold==f]
            #to be used for subsetting features for diff models
            X_train_temp=X_train_fold
            X_test_temp=X_test_fold
            this_fold_preds=[]
            for mm in range(len(self.models)):
                this_model=copy(self.models[mm])
                if len(self.feature_lists)==1:
                    X_train_temp=X_train_fold[self.feature_lists[0]]
                    X_test_temp=X_test_fold[self.feature_lists[0]]
                elif len(self.feature_lists)==len(self.models):
                    X_train_temp=X_train_fold[self.feature_lists[mm]]
                    X_test_temp=X_test_fold[self.feature_lists[mm]]
                #save the best estimator from cv that was then fit on all the data
                this_model.fit(X_train_temp,y_train_fold)
                if self.regression:
                    preds=this_model.predict(X_test_temp)
                else:
                    preds=this_model.predict_proba(X_test_temp)[:, 1]
                preds=np.reshape(preds,(len(preds),1))
                if mm==0:
                    this_fold_preds=preds
                else:
                    this_fold_preds=np.append(this_fold_preds, preds, axis=1)
            if len(oof_predictions)==0:
                oof_predictions=this_fold_preds
            else:
                oof_predictions=np.append(oof_predictions,this_fold_preds, axis=0)
            # Print shape
            if self.verbose > 1:
                print("Current Shape: "+ str(oof_predictions.shape))
        
        return oof_predictions

    # fit all models on entire data
    def fit_transform(self, X_train, y_train, cv=5, random_state=0):
        if self.verbose > 0:
            print("Inside fit_transform of StackLayer w/ #obs="+str(len(X_train))) 
        self.fit( X_train, y_train, random_state=random_state)
        
        if self.verbose > 0:
            print("Running out-of-fold predictions ")

        return self.get_oof_predictions(X_train, y_train, cv=cv)
            
    # fit all models on entire data
    def fit(self, X_train, y_train, random_state=0):
        if self.verbose > 0:
            print("Inside fit of StackLayer w/ #obs="+str(len(X_train)))
        X_temp=X_train

        #if feature lists not defined and only 1 model, just use the entire input
        if not self.feature_lists and len(self.models)==1:
            self.feature_lists=[list(X_train.columns)]

        # Print list of models
        if self.verbose > 1:
            print("List of models in Stack Layer: ")
            for mm in range(len(self.models)):
                print(self.models[mm])
        for mm in range(len(self.models)):
            if len(self.feature_lists)==1:
                X_temp=X_train[self.feature_lists[0]]
            elif len(self.feature_lists)==len(self.models):
                X_temp=X_train[self.feature_lists[mm]]
            #save the best estimator from cv that was then fit on all the data
            self.models[mm].fit(X_temp, y_train)
        
        
    # get predictions from all models
    def transform(self, X_test, y_test=None, metric=None):  
        if self.verbose > 0:    
            print("Inside transform of StackLayer w/ #obs="+str(len(X_test))) 
        if self.regression:
            return self.predict(X_test,y_test=y_test,metric=metric)
        else:
            return self.predict_proba(X_test,y_test=y_test,metric=metric)
    
    # get predictions from all models
    def predict(self, X_test, y_test=None, metric=None):
        if self.verbose > 0:
            print("Inside predict of StackLayer w/ #obs="+str(len(X_test)))
        pred_data=[]
        X_temp=X_test
        for mm in range(len(self.models)):
            if len(self.feature_lists)==1:
                X_temp=X_test[self.feature_lists[0]]
            elif len(self.feature_lists)==len(self.models):
                X_temp=X_test[self.feature_lists[mm]]
            #use the best estimator to create predictions
            pred=self.models[mm].predict(X_temp)
            pred=np.reshape(pred,(len(pred),1))
            if mm==0:
                pred_data=pred
            else:
                pred_data=np.append(pred_data, pred, axis=1)        
        return pred_data
    
    # get predictions from all models
    def predict_proba(self, X_test, y_test=None, metric=None):
        if self.verbose > 0:
            print("Inside predict_proba of StackLayer w/ #obs="+str(len(X_test)))
        pred_data=[]
        X_temp=X_test
        for mm in range(len(self.models)):
            if len(self.feature_lists)==1:
                X_temp=X_test[self.feature_lists[0]]
            elif len(self.feature_lists)==len(self.models):
                X_temp=X_test[self.feature_lists[mm]]
            #use the best estimator to create predictions
            pred=self.models[mm].predict_proba(X_temp)[:, 1]
            pred=np.reshape(pred,(len(pred),1))
            if mm==0:
                pred_data=pred
            else:
                pred_data=np.append(pred_data, pred, axis=1)        
        return pred_data
    
    # get predictions from all models
    def predict_log_proba(self, X_test, y_test=None, metric=None):
        if self.verbose > 0:
            print("Inside predict_log_proba of StackLayer w/ #obs="+str(len(X_test)))
        pred_data=[]
        X_temp=X_test
        for mm in range(len(self.models)):
            if len(self.feature_lists)==1:
                X_temp=X_test[self.feature_lists[0]]
            elif len(self.feature_lists)==len(self.models):
                X_temp=X_test[self.feature_lists[mm]]
            #use the best estimator to create predictions
            pred=self.models[mm].predict_log_proba(X_temp)[:, 1]
            pred=np.reshape(pred,(len(pred),1))
            if mm==0:
                pred_data=pred
            else:
                pred_data=np.append(pred_data, pred, axis=1)        
        return pred_data