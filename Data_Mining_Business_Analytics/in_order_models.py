# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 13:56:48 2023

@author: eloid
"""

#############################################################################
## Imports 
#############################################################################
import pandas as pd
import plotly as pl
from plotly.subplots import make_subplots
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, recall_score, precision_score, f1_score, accuracy_score
from sklearn.linear_model import LogisticRegression
from statistics import stdev
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.model_selection import StratifiedKFold
from scipy.stats import zscore
from sklearn.metrics import roc_curve, auc
from sklearn.ensemble import IsolationForest
from numpy import where
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from kmodes.kprototypes import KPrototypes
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import KElbowVisualizer
from yellowbrick.cluster import SilhouetteVisualizer



#############################################################################
## Data Loading 
#############################################################################
ks_original = pd.read_excel("C:\\Users\\eloid\\Documents\\School\\Classes\\Data Mining\\Individual Project\Kickstarter.xlsx")


#############################################################################
## 1: Understanding the data
#############################################################################
################################
# 1.1: Variables Inspection
################################
# Checking data types
## GOAL: Better understanding of all features available
ks_original.dtypes
        
# Descriptive statistics for numerical variables
desciptive_stats = ks_original.describe()


###################################################
# 1.2: Irrelevant, duplicates & missing values
###################################################
# Drop 'cancelled' or 'suspended' project
ks_original.info()
ks_original = ks_original.query("state in ('successful','failed')")
## NOTES: 2039 obs. dropped

# Checking duplicates
ks_original[ks_original.duplicated()].shape
## NOTES: No duplicates

# Missing values
## Analyze 'nan'
ks_original.info()
ks_original.isnull().sum()
## Notes: 1254 'nan' in 'category' (9% total obs.). Will treat it as a valid category bc insights could be derived from it.
ks_no_category = ks_original.drop('category', axis=1)
null_values = ks_no_category[ks_no_category.isnull().any(axis=1)]
## NOTES: Keep obs. 13042 bc only 'name' is missing (not 'name_len' & 'name_length_clean'), so would indicate an honest error.

## Reassign 'nan'
ks_original['category'] = ks_original['category'].fillna('missing')
## Verify
ks_original.isnull().sum()
## NOTES: no more 'nan'


###############################
# 1.3: Exploratory analysis
###############################
# Split categorical and numerical variables
## GOAL: Easier for data visualization and later use
categorical_original = ks_original.select_dtypes(include=['object', 'bool'])
numerical_original = ks_original.select_dtypes(exclude = ['object', 'bool'])

# Frequency tables for categorical variables (including 'nan)
## GOAL: Understand better distribution of dataset & locate missing values
categorical_frequency = {}
for column in categorical_original.columns:
    categorical_frequency[column] = pd.concat([ks_original[column].value_counts(dropna=False), ks_original[column].value_counts(dropna=False, normalize=True)], axis=1)

# Frequency tables for relevant numerical variables (including 'nan)
numerical_frequency = {}
state_over_numerical = {}
for column in ['name_len', 'blurb_len', 'backers_count']:
    numerical_frequency[column] = pd.concat([ks_original[column].value_counts(dropna=False), ks_original[column].value_counts(dropna=False, normalize=True)], axis=1)
    state_over_numerical[column] = pd.concat([ks_original.groupby('state')[column].value_counts(), ks_original.groupby('state')[column].value_counts(normalize = True)], axis=1) 

# Analyze relevance of 'name', 'name_len' & 'name_len_clean' 
name_vs_name_len = (len(ks_original['name']) == ks_original['name_len'])
## NOTES: 'name_len' never matches. 


# 1.3.1: Correlation matrix & heatmap
## GOAL: Analyze variable relationship
corr_numerical = numerical_original.corr()
#sns.heatmap(corr_numerical, cmap = "rocket_r", annot = False)
'''NOTES: 
    To watch: (excluding predictors that are going to be drop)
        blurb VS blurb_len_clean: 0.777
        launched_at_month VS created_at_month: [0.56, 0.60]   
'''

# 1.3.2: Boxplots for relevant numerical variables
## GOAL: visualize variables where outliers could be identified (using descriptive stats)
'''## NOTES: run every boxplots separately
sns.boxplot(x=ks_original['goal'])
sns.boxplot(x=ks_original['usd_pledged'])
sns.boxplot(x=ks_original['static_usd_rate'])
sns.boxplot(x=ks_original['backers_count'])
sns.boxplot(x=ks_original['name_len_clean'])
sns.boxplot(x=ks_original['blurb_len'])
sns.boxplot(x=ks_original['blurb_len_clean'])
sns.boxplot(x=ks_original['create_to_launch_days'])
'''

# 1.3.3: Histograms for relevant numerical variables
## GOAL: analyze skewness of distribution. Helpful to decide how to treat outliers
'''## NOTES: to run every plot separately
sns.histplot(x=ks_original['static_usd_rate'])
sns.histplot(x=ks_original['goal'], log_scale=True)
sns.histplot(x=ks_original['name_len_clean'])
sns.histplot(x=ks_original['blurb_len'], kde=True)
sns.histplot(x=ks_original['blurb_len_clean'], kde=True)
sns.histplot(x=ks_original['create_to_launch_days'], kde=True)
'''


# 1.3.4: Barchart with hue & proportion table for relevant categorical variables
## GOAL: Helpful to identify potential trend in predictors
''' ## NOTES: to run every plot separately
plt.figure(figsize=(15,20))
sns.countplot(x = 'country', data = ks_original, hue = "state")
sns.countplot(x = 'currency', data = ks_original, hue = "state")
sns.countplot(x = 'staff_pick', data = ks_original, hue = "state")
sns.countplot(x = 'category', data = ks_original,  hue = "state")
sns.countplot(x = 'spotlight', data = ks_original, hue = "state")
sns.countplot(x = 'deadline_weekday', data = ks_original, hue = "state")
sns.countplot(x = 'launched_at_weekday', data = ks_original, hue = "state")
sns.countplot(x = 'name_len', data = ks_original, hue = "state")
sns.countplot(x = 'blurb_len', data = ks_original, hue = "state")
'''

## Proportion table
categorical_over_state = {}
for variable in ['category', 'staff_pick', 'currency', 'country']:
    categorical_over_state[variable] = ks_original.groupby(variable)['state'].value_counts(normalize=True)
''' NOTES:
        staff_pick: 'success' when 'true': 0.78 VS 'false': 0.28
        spotlight: DROP: perfectly correlated with target variable
        country: 'LU' has 100% 'successful'
        category: 6 smallest category levels
            'Webseries', 'Thrillers', 'Shorts', 'Places', 'Academic': 100% 'failed'
            'Blues': 100% 'successful'
'''



#############################################################################
## 2: Pre-processing
#############################################################################
#######################################
# 2.1: Drop unnecessary variables
#######################################
# Simple identifier: 'id'
ks_original.drop(['id'], axis=1, inplace = True)
ks_original.drop(['name'], axis = 1, inplace = True)

# Highly correlated to target variable: 'spotlight'
ks_original.drop(['spotlight', 'backers_count'], axis=1, inplace = True)

# All variables (14) realized after the launch: deadline & state_changed_at
ks_original.drop(['deadline', 'state_changed_at', 'deadline_weekday', 'state_changed_at_weekday', 'deadline_month', 'deadline_day', 'deadline_yr', 'deadline_hr',
                  'state_changed_at_month', 'state_changed_at_day', 'state_changed_at_yr', 'state_changed_at_hr', 'launch_to_deadline_days', 'launch_to_state_change_days'], axis=1, inplace = True)

## Realized at time of data scrape: 'pledged' & 'usd_pledged': 
ks_original.drop(['pledged', 'usd_pledged'], axis=1, inplace = True)

# Inaccurate: 'name_len' & 'name_len_clean'
ks_original.drop(['name_len', 'name_len_clean'], axis=1, inplace = True)

# Unary variables or rows
ks_original.drop(columns = ks_original.columns[ks_original.nunique() == 1], inplace=True)
## NOTES: 'disable_communication' dropped

# Convert 'goal' in usd
ks_original['goal_usd'] = ks_original['goal'] * ks_original['static_usd_rate']
ks_original = ks_original.drop(['goal'], axis = 1)

# Timestamp predictors
dummy_launched_at = pd.to_datetime(ks_original['launched_at']).sort_values(ascending = True)
ks_original['launched_at'] = (dummy_launched_at - dummy_launched_at.iloc[0])/pd.to_timedelta('1Min')
dummy_created_at = pd.to_datetime(ks_original['created_at']).sort_values(ascending = True)
ks_original['created_at'] = (dummy_created_at - dummy_created_at.iloc[0])/pd.to_timedelta('1Min')
# NOTES: timestamp object was converted in a float delta (from oldest project)
''' NOTES:
        I wasn't able to properly convert in seconds, which was the unit precision used here. 
'''

######################################
# 2.2: Variable recoding & cleaning
######################################
## GOAL: Useful for data manipulation and comparison
dummy_ks = ks_original.copy()

# Target variable
dummy_ks['state'] = dummy_ks['state'].replace({'successful': 1, "failed": 0})

# Binary predictors
dummy_ks = dummy_ks.astype({"staff_pick": 'int64'})


# 2.1: Dummify categorical variables & drop appropriate level
''' NOTES:
        Although it's mentionned that Random Forest and Gradient Boosting don't 
        require categorical variables to be dummified, we are still going to perform it. 
        So we can use Logistic Regression as a base model for comparison. 
    '''
## GOAL: Better interpretability than simply dropping first level
dummy_category = pd.get_dummies(dummy_ks[['category']])
dummy_category.drop('category_missing', axis = 1, inplace = True)

dummy_country = pd.get_dummies(dummy_ks[['country']])
dummy_country.drop('country_US', axis = 1, inplace = True)

dummy_currency = pd.get_dummies(dummy_ks[['currency']])
dummy_currency.drop('currency_USD', axis = 1, inplace = True)

dummy_created_at_weekday = pd.get_dummies(dummy_ks[['created_at_weekday']])
dummy_created_at_weekday.drop('created_at_weekday_Sunday', axis = 1, inplace = True)

dummy_launched_at_weekday = pd.get_dummies(dummy_ks[['launched_at_weekday']])
dummy_launched_at_weekday.drop('launched_at_weekday_Sunday', axis = 1, inplace = True)

## Create dummified dataset
## GOAL: will be used in our test-train split
dummy_ks = pd.concat([dummy_ks, dummy_category, dummy_country, dummy_currency, dummy_created_at_weekday, dummy_launched_at_weekday], axis=1)
dummy_ks = dummy_ks.select_dtypes(exclude=['object'])


#############################
# 2.3: Splitting dataset
#############################
# Construct variables
X = dummy_ks.drop(['state'], axis=1)
y = dummy_ks['state']

# Train-test split 
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify = y, test_size = 0.33, random_state = 16)




#############################################################################
# 3: Base Model & Cross Validation method
#############################################################################
## GOAL: Ensure other models are performing properly by comparing with base model

# Cross Validation method
k_fold = StratifiedKFold(n_splits = 5, shuffle = True, random_state = 16)

def evaluate_model(model, model_type : str, y_pred, X_train, X_test, y_train, y_test, k_fold):
    ''' Train, predict and outputs a summary of the model's performance metrics 
        depending on the state and type of the model.
    '''
    # Evaluation measures
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Cross-Validation
    cv_scores = cross_val_score(model, X_train, y_train, cv = k_fold, scoring = 'accuracy')
    avg_cv_score = cv_scores.mean()

    # Metrics Visualization
    df_ = [(accuracy, precision, recall, f1, avg_cv_score)]
    performance = pd.DataFrame(data = df_, columns = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'Avg CV Accuracy'])
    performance.insert(0, 'Models', model_type)
    return performance

# Build, train, predict and evaluate - Base model
lr_base = LogisticRegression()
lr_base.fit(X_train, y_train)
y_pred_lr = lr_base.predict(X_test)
performance_models = evaluate_model(lr_base, 'Logistic Regression - Base model', y_pred_lr, X_train, X_test, y_train, y_test, k_fold)



#############################################################################
# 4: Classification Model 1 - Random Forest
#############################################################################
# Build, train, predict
randomforest = RandomForestClassifier(n_estimators = 50, random_state = 16)
randomforest.fit(X_train, y_train)
y_pred_rf = randomforest.predict(X_test)

# Cross-validate & evaluate
performance_rf = evaluate_model(randomforest, 'Random Forest - Before tuning hyperparameters', y_pred_rf, X_train, X_test, y_train, y_test, k_fold)
performance_models = pd.concat([performance_models, performance_rf], ignore_index = True, sort = False)

# Confusion matrix
confusion_matrix_rf = confusion_matrix(y_test, y_pred_rf)



################################
# 4.1: Hyperparameter tuning
################################
## GOAL: Using GridSearchCV, determine values of hyperparameters that optimize the accuracy
'''NOTES:
initial params_rf = {
    'n_estimators': [300, 400, 500],
    'max_features': [5, 7, 9, 11],
    'min_samples_split': [1, 2, 3],
    'min_samples_leaf': [5, 7 ,9],
    'random_state': [16]
}
'''
# Find optimal hyperparameters
'''
params_rf = {
    'n_estimators': [256],
    'max_features': [9],
    'min_samples_split': [2],
    'min_samples_leaf': [2],
    'random_state': [16]
}

grid_rf = GridSearchCV(randomforest, param_grid = params_rf, cv = k_fold, scoring = 'accuracy', n_jobs = -1).fit(X_train, y_train)
tuned_rf_best_params = grid_rf.best_params_
tuned_rf_best_score = grid_rf.best_score_
print('Best parameters:', tuned_rf_best_params)
print('Best score:', tuned_rf_best_score)
'''

# Predict with optimal hyperparameters
randomforest_tuned = RandomForestClassifier(random_state = 16, max_features = 9, n_estimators = 256, min_samples_split = 2, min_samples_leaf = 2)
randomforest_tuned.fit(X_train, y_train)
y_pred_rf = randomforest_tuned.predict(X_test)

# Cross-validate, evaluate & compare
performance_tuned_rf = evaluate_model(randomforest_tuned, 'Random Forest - After tuning hyperparameters', y_pred_rf, X_train, X_test, y_train, y_test, k_fold)
performance_rf = pd.concat([performance_rf, performance_tuned_rf], ignore_index = True, sort = False)
performance_models = pd.concat([performance_models, performance_tuned_rf], ignore_index = True, sort = False)



###################
# 4.2: Outliers
###################
# GOAL: Compare model performance with and without outliers

# Isolation forest (contamination = 0.02)
iforest = IsolationForest(n_estimators = 100, contamination = 0.02)
pred_iforest = iforest.fit_predict(dummy_ks)
# Extracting anomalies
anomaly_index = where(pred_iforest == -1)
anomaly_index = anomaly_index[0]

# Removing anomalies from initial data split
X_test_no_outliers = X_test.loc[~X_test.index.isin(anomaly_index)]
y_test_no_outliers = y_test.loc[~y_test.index.isin(anomaly_index)]
X_train_no_outliers = X_train.loc[~X_train.index.isin(anomaly_index)]
y_train_no_outliers = y_train.loc[~y_train.index.isin(anomaly_index)]


# Train & predict without outliers
randomforest_tuned_no_outliers = randomforest_tuned.fit(X_train_no_outliers, y_train_no_outliers)
y_pred_rf = randomforest_tuned_no_outliers.predict(X_test_no_outliers)

# Cross-validate, evaluate & compare
performance_tuned_no_outliers_rf = evaluate_model(randomforest_tuned_no_outliers, 'Random Forest - Whithout outliers', y_pred_rf, X_train_no_outliers, X_test_no_outliers, y_train_no_outliers, y_test_no_outliers, k_fold)
performance_rf = pd.concat([performance_rf, performance_tuned_no_outliers_rf], ignore_index = True, sort = False)
performance_models = pd.concat([performance_models, performance_tuned_no_outliers_rf], ignore_index = True, sort = False)

''' NOTES:  2% contamination rate: 231 obs removed
                --> Accuracy (training and test data): slightly decreased
'''


################################
# 4.3: Feature Selection
################################
# Feature importance
pd.Series(randomforest_tuned.feature_importances_, index = X.columns).sort_values(ascending = False).plot(kind = 'bar', figsize = (14,6))
feature_importance_rf = pd.DataFrame(list(zip(X.columns, randomforest_tuned.feature_importances_)), columns = ['predictor','feature importance'])

# Train and predict using new dataframe
X_train_final_rf = X_train[['goal_usd', 'staff_pick', 'create_to_launch_days', 'launched_at', 'created_at']]
X_test_final_rf = X_test[['goal_usd', 'staff_pick', 'create_to_launch_days', 'launched_at', 'created_at']]
randomforest_selected = randomforest_tuned.fit(X_train_final_rf, y_train)
y_pred_rf = randomforest_selected.predict(X_test_final_rf)

# Cross-validate, evaluate & compare
performance_selected_rf = evaluate_model(randomforest_selected, 'Random Forest - After Feature Selection', y_pred_rf, X_train_final_rf, X_test_final_rf, y_train, y_test, k_fold)
performance_rf = pd.concat([performance_rf, performance_selected_rf], ignore_index = True, sort = False)
performance_models = pd.concat([performance_models, performance_selected_rf], ignore_index = True, sort = False)

''' NOTES:
        Feature importance min. threshold of 5%:
            From 76 predictors to 5 predictors (highly reduced complexity of model)
                --> Accuracy (training and test data): decreased by 4-6%
'''

#########################################
# 4.4: Further evaluation of the model
#########################################
# Predict probabilities on the test set
y_prob_rf = randomforest_selected.predict_proba(X_test_final_rf)[:, 1]

# Calculate ROC curve and AUC
fpr, tpr, thresholds = roc_curve(y_test, y_prob_rf)
roc_auc = auc(fpr, tpr)

# Plot the ROC curve
plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve - Random Forest')
plt.legend(loc='lower right')
plt.show()



#############################################################################
# 5: Classification Model 2 - Gradient Boosting
#############################################################################
# Build, train, predict
gbt = GradientBoostingClassifier(n_estimators = 50, random_state = 16)
gbt.fit(X_train, y_train)
y_pred_gbt = gbt.predict(X_test)

# Cross-validate & evaluate
performance_gbt = evaluate_model(gbt, 'Gradient Boosting - Before tuning hyperparameters', y_pred_gbt, X_train, X_test, y_train, y_test, k_fold)
performance_models = pd.concat([performance_models, performance_gbt], ignore_index = True, sort = False)

# Confusion matrix & Evaluation measures
confusion_matrix_gbt = confusion_matrix(y_test, y_pred_gbt)



################################
# 5.1: Hyperparameter tuning
################################
## GOAL: Using GridSearchCV, determine values of hyperparameters that optimize the accuracy
'''NOTES:
initial params_gbt = {
    'n_estimators': [300, 400, 500],
    'max_features': [5, 7, 9, 11],
    'min_samples_split': [1, 2, 3],
    'min_samples_leaf': [5, 7, 9],
}
'''
# Find optimal hyperparameters
'''
params_gbt = {
    'n_estimators': [298],
    'max_features': [9],
    'min_samples_split': [2],
    'min_samples_leaf': [3],
    'random_state': [16]
}
grid_gbt = GridSearchCV(gbt, param_grid = params_gbt, cv = k_fold, scoring = 'accuracy', n_jobs = -1).fit(X_train, y_train)
print('Best parameters:', grid_gbt.best_params_)
print('Best score:', grid_gbt.best_score_)
'''

# Predict with optimal hyperparameters
gbt_tuned = GradientBoostingClassifier(random_state = 16, max_features = 9, n_estimators = 298, min_samples_split = 2, min_samples_leaf = 3)
gbt_tuned.fit(X_train, y_train)
y_pred_gbt = gbt_tuned.predict(X_test)

# Cross-validate, evaluate & compare
performance_tuned_gbt = evaluate_model(gbt_tuned, 'Gradient Boosting - After tuning hyperparameters', y_pred_gbt, X_train, X_test, y_train, y_test, k_fold)
performance_gbt = pd.concat([performance_gbt, performance_tuned_gbt], ignore_index = True, sort = False)
performance_models = pd.concat([performance_models, performance_tuned_gbt], ignore_index = True, sort = False)



###################
# 5.2: Outliers
###################
# GOAL: Compare model performance with and without outliers

# Train & predict without outliers
gbt_tuned_no_outliers = gbt_tuned.fit(X_train_no_outliers, y_train_no_outliers)
y_pred_gbt = gbt_tuned_no_outliers.predict(X_test_no_outliers)

# Cross-validate, evaluate & compare
performance_tuned_no_outliers_gbt = evaluate_model(gbt_tuned_no_outliers, 'Gradient Boosting - Whithout outliers', y_pred_gbt, X_train_no_outliers, X_test_no_outliers, y_train_no_outliers, y_test_no_outliers, k_fold)
performance_gbt = pd.concat([performance_gbt, performance_tuned_no_outliers_gbt], ignore_index = True, sort = False)
performance_models = pd.concat([performance_models, performance_tuned_no_outliers_gbt], ignore_index = True, sort = False)

''' NOTES:  2% contamination rate: 231 obs removed
                --> Accuracy (training and test data): slightly decreased
'''


################################
# 5.3: Feature Selection
################################
# Feature importance
pd.Series(gbt_tuned.feature_importances_, index = X.columns).sort_values(ascending = False).plot(kind = 'bar', figsize = (14,6))
feature_importance_gbt = pd.DataFrame(list(zip(X.columns, gbt_tuned.feature_importances_)), columns = ['predictor','feature importance'])

# Train and predict using new dataframe
X_train_final_gbt = X_train[['staff_pick', 'category_Web', 'category_Software', 'goal_usd', 'create_to_launch_days', 'launched_at']]
X_test_final_gbt = X_test[['staff_pick', 'category_Web', 'category_Software', 'goal_usd', 'create_to_launch_days', 'launched_at']]
gbt_selected = gbt_tuned
gbt_selected.fit(X_train_final_gbt, y_train)
y_pred_gbt = gbt_selected.predict(X_test_final_gbt)

# Cross-validate, evaluate & compare
performance_selected_gbt = evaluate_model(gbt_selected, 'Gradient Boosting - After Feature Selection', y_pred_gbt, X_train_final_gbt, X_test_final_gbt, y_train, y_test, k_fold)
performance_gbt = pd.concat([performance_gbt, performance_selected_gbt], ignore_index = True, sort = False)
performance_models = pd.concat([performance_models, performance_selected_gbt], ignore_index = True, sort = False)

''' NOTES:
        Feature importance min. threshold of 0.05:
            From 74 predictors to 5 predictors (highly reduced complexity of model)
                --> Accuracy on training data: -2.07% (77.77% to 75.70%)
                --> Accuracy on test data: -3.20% (78.08% to 74.88%)
        Feature importance min. threshold of 0.045:
            From 74 predictors to 6 predictors (highly reduced complexity of model)
                --> Accuracy on training data: -1.62% (77.77% to 76.14%)
                --> Accuracy on test data: -3.07% (78.08% to 75.01%)
                
            Decision: keep 6 predictors
'''

#########################################
# 5.4: Further evaluation of the model
#########################################
# Predict probabilities on the test set
y_prob_gbt = gbt_selected.predict_proba(X_test_final_gbt)[:, 1]

# Calculate ROC curve and AUC
fpr, tpr, thresholds = roc_curve(y_test, y_prob_gbt)
roc_auc = auc(fpr, tpr)

# Plot the ROC curve
plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve - Gradient Boosting')
plt.legend(loc='lower right')
plt.show()





#############################################################################
## 7: Clustering Model
#############################################################################
#####################################################
# 7.1: Transformation of data & selection of model
#####################################################
X_ = X.astype({"staff_pick": 'bool'})

# Remove outliers
## GOAL: better interpretability of the clusters
'''
iforest = IsolationForest(n_estimators = 100, contamination = 0.02)
pred_iforest = iforest.fit_predict(X_)
anomaly_index = where(pred_iforest == -1)
anomaly_index = anomaly_index[0]
X_ = X_.loc[~X_.index.isin(anomaly_index)]
'''

# Standardize numerical features
X_numerical = X_.select_dtypes(exclude = ['bool'])
scaler = MinMaxScaler()
X_numerical_std = scaler.fit_transform(X_numerical)
X_numerical_std = pd.DataFrame(X_numerical_std, columns = X_numerical.columns) 

## Standardized & Dummified 
X_categorical = ks_original.select_dtypes(include=['object', 'bool'])
X_categorical.drop(['state'], axis = 1, inplace = True)
X_numerical_std.reset_index(drop=True, inplace=True)
X_categorical.reset_index(drop=True, inplace=True)
X_std = pd.merge(X_numerical_std, X_categorical, left_index=True, right_index=True)

## Standardized but no dummies
X_dum_categorical = X_.select_dtypes(exclude=['int64', 'float'])
X_numerical_std.reset_index(drop=True, inplace=True)
X_dum_categorical.reset_index(drop=True, inplace=True)
X_dum_std = pd.merge(X_numerical_std, X_dum_categorical, left_index = True, right_index = True)


# Reduce to 2 dimensions (PCA) for visualization
pca = PCA(n_components = 2)
X_pca = pca.fit_transform(X_dum_std)
X_pca = pd.DataFrame(X_pca, columns =['PC1', 'PC2']) 
plt.scatter(X_pca['PC1'], X_pca['PC2'])
plt.xlabel("PC 1")
plt.ylabel("PC 2")
plt.show()

''' NOTES: Potentially 6 uniform clusters: K-means or K-Protoype is acceptable
'''


##############################
# 7.2: Determination of 'k'
##############################
# Elbow method
withinss = []
for i in range (2, 12):    
    kmeans = KMeans(n_clusters = i, init = 'k-means++', n_init = 'auto', random_state = 21)
    kmeans.fit(X_dum_std)
    withinss.append(kmeans.inertia_)
    
plt.plot(range(2, 12), withinss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Withinss')
plt.show()

## Distortion score Elbow
model = KMeans(init = 'k-means++', n_init = 'auto', random_state = 21)
visualizer = KElbowVisualizer(model, k=(2, 15), timings= True)
visualizer.fit(X_dum_std)
visualizer.show()  


# Silhouette visualization
fig, ax = plt.subplots(3, 2, figsize=(13,8))
fig.suptitle('Silhouette Analysis for 2-7 Clusters', size = 18)
plt.tight_layout()
for i in [2, 3, 4, 5, 6, 7]:
    km = KMeans(n_clusters=i, init = 'k-means++', n_init = 5, max_iter = 30, random_state = 21)
    q, mod = divmod(i, 2)
    visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax = ax[q-1][mod])
    visualizer.fit(X_dum_std)

''' NOTES:
        Based on both analysis of Elbow and Silouhette methods, optimal k: 4 or 6 clusters
'''



##############################
# 7.3: Build, Train, Predict
##############################
k = 4
# Final K-Prototype Model
kmixed = KPrototypes(n_clusters = k, init = 'random', n_init = 1, random_state = 21, max_iter = 40, verbose = True)
clusters_proto = kmixed.fit_predict(X_std, categorical=[15,16,17,18,19,20])

# Assign cluster labels to the original dataframe
X_['Cluster'] = clusters_proto

# Distribution of the clusters
plt.figure(figsize = (10, 6))
plot = sns.countplot(x = X_["Cluster"], palette = 'Set1')
plt.show()

## Plot clusters
plt.figure(figsize = (10, 6))
sns.scatterplot(x = X_pca['PC1'], y = X_pca['PC2'], data = X_, hue = 'Cluster', palette = 'Set1')
plt.title(f'K-Means Clustering with {k} Clusters')
plt.xlabel("PC 1")
plt.ylabel("PC 2")
plt.legend()
plt.show()



##############################
# 7.4: Analysis of clusters
##############################
# Boxplot for numerical variables
for feature in X_numerical.columns:
    plt.figure(figsize = (10, 6))
    sns.boxplot(x = X_['Cluster'], y = feature, data = X_, palette = 'Set1')
    plt.title(f'{feature} Distribution Across Clusters')
    plt.show()

# Histogram for numerical variables
for feature in X_numerical.columns:
    plt.figure(figsize = (10, 6))
    sns.histplot(x = X_['Cluster'], y = feature, data = X_, palette = 'Set1')
    plt.title(f'{feature} Distribution Across Clusters')
    plt.show()
    
# Countplot for categorical features
'''
for feature in X_categorical.columns:
    plt.figure(figsize = (10, 6))
    sns.countplot(x = feature, hue = 'Cluster', data = X_, palette = 'Set1')
    plt.title(f'{feature} Distribution Across Clusters')
    plt.show()
'''
''' NOTES: 
        'created_at', 'launched_at', 'created_at_yr', 'launched_at_yr': 
                cluster (1): older projects
        
        'launched_at_day', 'created_at_day':
                cluster (3): later in the month
                cluster(0): a bit earlier in the month
                
        'launched_at_month', 'created_at_month':
                cluster(2): projects launched/created earlier in the year
                
                
        
        MAYBE???        
        'static_usd_rate': 
                cluster (1): projects with higher usd rate
        
        
        'created_to_launch_days':
                cluster (1): shorter period
        'blurb_len', 'blurb_len_clean': 
                cluster (1): no outliers on the upper bound
                
        'currency_GBP', 'country_GB':
                cluster(1): all the successful projects are in this cluster
                
        'launched_at_weekday_Monday': 
                cluster(2): 100% successful projects in this cluster
                cluster(0-2): 100% of the successful projects between those 2 clusters
    
'''

# To analyze relationship between features (by clusters)
'''
plt.figure(figsize=(15,7))
sns.scatterplot(data = X_, x = 'launched_at_yr', y = 'launched_at', hue = 'Cluster', s = 15, palette = 'Set1')
'''
