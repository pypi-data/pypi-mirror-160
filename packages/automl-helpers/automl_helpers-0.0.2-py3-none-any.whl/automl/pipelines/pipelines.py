'''
Description: this file contains sklearn pipelines to be used for automated machine learning


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
from sklearn.metrics import mean_absolute_error, accuracy_score, log_loss, make_scorer, roc_auc_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils.multiclass import unique_labels
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import sklearn
if sklearn.__version__<'0.20':
    from sklearn.cross_validation import train_test_split, KFold, StratifiedKFold, PredefinedSplit
else:
    from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, PredefinedSplit

from automl import automl_utils
from automl import StackLayer, TextElasticNetBinary, MissingDataHandler

# CHANGE TO OUTPUT A DICTIONARY
def tfidf_enet_stacklayer(X_train,y_train,text_features,cv=5,verbose=0):
    sss=[] #list containing each stacked elastic net
    text_features_out=[] #list containing each output text feature name
    drop_text_list=[]

    for feat in list(text_features):    
        print(feat)
        if X_train[feat].nunique()>1:
            text_features_out.append(feat)
            sss_temp=StackLayer(models=[TextElasticNetBinary(token_pattern=r'(?u)\b\w+\b')],feature_lists=[feat], gridsearch_lists=[{'penalty_C':list(np.arange(1,10.1,4)),'ngram_range':list([(1, 1),(1,2)])}],regression=False,verbose=0)
            sss_temp.tune_hyperparameters(X_train, y_train, metric=None, n_jobs=1, cv=cv)
            sss.append(sss_temp)
        else:
            print("Not unique values for "+feat)
            drop_text_list.append([feat])
    return sss, text_features_out


def gbm_classifier_pipeline(X_train,y_train,num_features,text_features,scoring='neg_log_loss',cv=5,verbose=0):

    #if text features build pretrained layer
    if len(text_features)>0:
        sss, text_features_out=tfidf_enet_stacklayer(X_train,y_train,text_features,cv=5,verbose=0)

    mmm=MissingDataHandler(method='median',create_dummy=True)

    gbm=GradientBoostingClassifier(learning_rate=.05,random_state=1234)

    pipe = Pipeline(
        [   ("Preprocessing",ColumnTransformer([( "MissingNumeric", mmm, num_features)]+[("TextStacking_#"+text_features_out[fff], sss[fff], [text_features_out[fff]]) for fff in range(len(text_features_out))])),
            # Use a SVC classifier on the combined features
            ("gbm", gbm),
        ],
        verbose=verbose,
    )

    param_grid = {
        "gbm__n_estimators": list(range(100,201,100)),
        'gbm__max_depth':list(range(3,6,2))
    }
    search = GridSearchCV(pipe, param_grid,scoring=scoring, n_jobs=None,verbose=1)
    search.fit(X_train[num_features+[fff for fff in text_features_out]], y_train)
    print("Best parameter (CV score=%0.3f):" % search.best_score_)
    print(search.best_params_)

    return search.best_estimator_

def rf_classifier_pipeline(X_train,y_train,num_features,text_features,scoring='neg_log_loss',cv=5,verbose=0):

    #if text features build pretrained layer
    if len(text_features)>0:
        sss, text_features_out=tfidf_enet_stacklayer(X_train,y_train,text_features,cv=5,verbose=0)

    mmm=MissingDataHandler(method='median',create_dummy=True)

    rf=RandomForestClassifier(max_samples=.5,min_samples_leaf=5,random_state=1234)

    pipe2 = Pipeline(
        [   ("Preprocessing",ColumnTransformer([( "MissingNumeric", mmm, num_features)]+[("TextStacking_#"+text_features_out[fff], sss[fff], [text_features_out[fff]]) for fff in range(len(text_features_out))])),
            # Use a SVC classifier on the combined features
            ("rf", rf),
        ],
        verbose=verbose,
    )

    param_grid = {
        "rf__n_estimators": list(range(200,301,100)),
        'rf__max_leaf_nodes':list([8,16,32,64])#
    }
    search2 = GridSearchCV(pipe2, param_grid,scoring=scoring ,n_jobs=None,verbose=1)
    search2.fit(X_train[num_features+[fff for fff in text_features_out]], y_train)
    print("Best parameter (CV score=%0.3f):" % search2.best_score_)
    print(search2.best_params_)

    return search2.best_estimator_


def all_tree_classifier_pipeline(X_train,y_train,num_features,text_features,scoring='neg_log_loss',cv=5,verbose=0):

    #if text features build pretrained layer
    if len(text_features)>0:
        sss, text_features_out=tfidf_enet_stacklayer(X_train,y_train,text_features,cv=5,verbose=0)

    mmm=MissingDataHandler(method='median',create_dummy=True)

    gbm=GradientBoostingClassifier(learning_rate=.05,random_state=1234)

    pipe = Pipeline(
        [   ("Preprocessing",ColumnTransformer([( "MissingNumeric", mmm, num_features)]+[("TextStacking_#"+text_features_out[fff], sss[fff], [text_features_out[fff]]) for fff in range(len(text_features_out))])),
            # Use a SVC classifier on the combined features
            ("gbm", gbm),
        ],
        verbose=verbose,
    )

    param_grid = {
        "gbm__n_estimators": list(range(100,201,100)),
        'gbm__max_depth':list(range(3,6,2))
    }
    search = GridSearchCV(pipe, param_grid,scoring=scoring ,n_jobs=None,verbose=1)
    search.fit(X_train[num_features+[fff for fff in text_features_out]], y_train)
    print("Best parameter (CV score=%0.3f):" % search.best_score_)
    print(search.best_params_)


    rf=RandomForestClassifier(max_samples=.5,min_samples_leaf=5,random_state=1234)

    pipe2 = Pipeline(
        [   ("Preprocessing",ColumnTransformer([( "MissingNumeric", mmm, num_features)]+[("TextStacking_#"+text_features_out[fff], sss[fff], [text_features_out[fff]]) for fff in range(len(text_features_out))])),
            # Use a SVC classifier on the combined features
            ("rf", rf),
        ],
        verbose=verbose,
    )

    param_grid = {
        "rf__n_estimators": list(range(100,301,100)),
        'rf__max_leaf_nodes':list([8,16,32,64])
    }
    search2 = GridSearchCV(pipe2, param_grid,scoring=scoring ,n_jobs=None,verbose=1)
    search2.fit(X_train[num_features+[fff for fff in text_features_out]], y_train)
    print("Best parameter (CV score=%0.3f):" % search2.best_score_)
    print(search2.best_params_)

    return [search.best_estimator_,search2.best_estimator_]


class XGBoostWithEarlyStop(BaseEstimator):
    def __init__(self, early_stopping_rounds=5, test_size=0.1, 
                 eval_metric='mae', **estimator_params):
        self.early_stopping_rounds = early_stopping_rounds
        self.test_size = test_size
        self.eval_metric=eval_metric='mae'        
        if self.estimator is not None:
            self.set_params(**estimator_params)

    def set_params(self, **params):
        return self.estimator.set_params(**params)

    def get_params(self, **params):
        return self.estimator.get_params()

    def fit(self, X, y):
        x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=self.test_size)
        self.estimator.fit(x_train, y_train, 
                           early_stopping_rounds=self.early_stopping_rounds, 
                           eval_metric=self.eval_metric, eval_set=[(x_val, y_val)])
        return self

    def predict(self, X):
        return self.estimator.predict(X)

class XGBoostRegressorWithEarlyStop(XGBoostWithEarlyStop):
    def __init__(self, *args, **kwargs):
        self.estimator = XGBRegressor()
        super(XGBoostRegressorWithEarlyStop, self).__init__(*args, **kwargs)

class XGBoostClassifierWithEarlyStop(XGBoostWithEarlyStop):
    def __init__(self, *args, **kwargs):
        self.estimator = XGBClassifier()
        super(XGBoostClassifierWithEarlyStop, self).__init__(*args, **kwargs)



# class E2EPipeline(Pipeline):
#     def predict(self, X, **predict_params):
#         """Applies transforms to the data, and the predict method of the
#         final estimator. Valid only if the final estimator implements
#         predict."""
#         Xt = X
#         for name, transform in self.steps[:-1]:
#             Xt = transform.transform(Xt)
#         return self.steps[-1][-1].predict(Xt, **predict_params)


# class E2EPipeline(BaseEstimator):
#     def __init__():
#         self.early_stopping_rounds = early_stopping_rounds
#         self.test_size = test_size
#         self.eval_metric=eval_metric='mae'        
#         if self.estimator is not None:
#             self.set_params(**estimator_params)

#     def set_params(self, **params):
#         return self.estimator.set_params(**params)

#     def get_params(self, **params):
#         return self.estimator.get_params()

#     def fit(self, X, y):
#         x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=self.test_size)
#         self.estimator.fit(x_train, y_train, 
#                            early_stopping_rounds=self.early_stopping_rounds, 
#                            eval_metric=self.eval_metric, eval_set=[(x_val, y_val)])
#         return self

#     def predict(self, X):
#         return self.estimator.predict(X)
