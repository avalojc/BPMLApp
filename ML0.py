from flask import Flask
import sklearn.linear_model
from sklearn.linear_model import LogisticRegression
import joblib
import random
import pandas as pd
# import gcsfs

# define  csv being read
url = pd.read_csv('gs://javalo-nhanes-bucket-cen/NHANESbpLabeled.csv')
df = pd.read_csv(url)
#feature vectors for comparison
include = ['BPACSZ2',	'BPACSZ3',	'BPACSZ4',	'BPACSZ5',	'BPXPLS',	'BPXPULS', 'SysRiskLevels'] 
df_ = df[include]

# Data Preprocessing
categoricals = []
for col, col_type in df_.dtypes.iteritems():
     if col_type == 'O':
          categoricals.append(col)
     else:
          df_[col].fillna(0, inplace=True)

df_ohe = pd.get_dummies(df_, columns=categoricals, dummy_na=True)

# run a logistical regression
dependent_variable = 'SysRiskLevels'
x = df_ohe[df_ohe.columns.difference([dependent_variable])]
y = df_ohe[dependent_variable]
lr = LogisticRegression()
lr.fit(x, y)

# Save the model
joblib.dump(lr, 'model.pkl')
print("Model dumped!")

# Load the model
lr = joblib.load('model.pkl')

# Saving the colums
model_columns = list(x.columns)
joblib.dump(model_columns, 'model_columns.pkl')
print("Models columns dumped!")