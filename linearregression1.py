# -*- coding: utf-8 -*-
"""boranislamoglu_ML_HW4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bn3oYwBcqLXqPPs5WzphHrGPCtVfJG6Y

# Load the dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt                   

df = pd.read_csv('https://raw.githubusercontent.com/OpenClassrooms-Student-Center/Evaluate-Improve-Models/master/house_prices.csv')
df.sample(5)

"""# "Garage Area" and "SalesPrice" features are selected to analyze."""

new_df = df[['Garage Area','SalesPrice']]
new_df.sample(5)

"""## Convert the data into numpy arrays of two variables, X and y.

---
"""

X = np.array(new_df[['Garage Area']])
y = np.array(new_df[['SalesPrice']])
print(X.shape) # Vewing the shape of X
print(y.shape) # Vewing the shape of y

"""## Split train and test data with 0.2 ratio."""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

"""# Linear Regression
Train a linear regression.
"""

from sklearn import linear_model 

regressor = linear_model.LinearRegression()

regressor.fit(X_train,y_train)

"""## Calculate train and test R2."""

from sklearn.metrics import r2_score

y_train_pred = regressor.predict(X_train)
print("Train:", r2_score(y_train,y_train_pred))

y_pred = regressor.predict(X_test)
print("Test:", r2_score(y_test,y_pred))

"""## Print the bias and the slope."""

print('Regressor coeffient or slope:',regressor.coef_[0][0])
print('Interception point with axis:',regressor.intercept_[0])

"""## Plot the test set with scatter plot and add the linear regression model line.
Remember linear regression recitation.
"""

# Plot a graph with X_test vs y_test
plt.scatter(X_test,y_test,color="aqua")
# Regressior line showing
plt.plot(X_test,regressor.predict(X_test),color="red",linewidth=3)
plt.title('Regression(Test Set)')
plt.xlabel('Garage Area')
plt.ylabel('SalesPrice')
plt.show()

"""# Multiple Linear Regression
Select all features.
"""

X1 = np.array(df.drop('SalesPrice', axis=1))
y1 = np.array(df['SalesPrice'])
print(X1.shape) # Vewing the shape of X
print(y1.shape) # Vewing the shape of y

"""## Rescale the input features. Use MinMaxScaler."""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X1 = scaler.fit_transform(X1)

"""## Train test split."""

from sklearn.model_selection import train_test_split
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2)

"""## Fit regression model."""

regressor = linear_model.LinearRegression()

regressor.fit(X1_train,y1_train)

"""## Calculate train and test R2."""

y1_train_pred = regressor.predict(X1_train)
print("Train:", r2_score(y1_train,y1_train_pred))

y1_pred = regressor.predict(X1_test)
print("Test:", r2_score(y1_test,y1_pred))

"""## Print the regression coefficients."""

i = 0
while(i < 304):
  print('Regressor coeffients for multiple linear regression:',regressor.coef_[i])
  i = i+1

"""# Ridge Regression
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html

https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html

## Use cross-validation to estimate alpha. Set the fold size to 5.
"""

from sklearn.model_selection import KFold
from sklearn.linear_model import RidgeCV
kfold = KFold(n_splits=5)
max = 0
bestalpha = 0
for train_index, test_index in kfold.split(X1_train):
  alphas=[1e-3, 1e-2, 1e-1, 1, 2, 5, 8, 10]
  for i in alphas:
    clf = linear_model.LinearRegression()
    clf = RidgeCV([i]).fit(X1_train[train_index],y1_train[train_index])
    score = r2_score(y1_train[test_index],clf.predict(X1_train[test_index]))
    if(score > max):
      max = score
      bestalpha = i

"""## Calculate the train and test R2."""

clf = RidgeCV([bestalpha]).fit(X1_train,y1_train)
y1_train_pred = clf.predict(X1_train)
print("Train:", r2_score(y1_train,y1_train_pred))

y1_pred = clf.predict(X1_test)
print("Test:", r2_score(y1_test,y1_pred))

"""## Print the best alpha."""

print("Alpha:", bestalpha) #bestalpha calculated in k-fold cell.

"""## Print the regression coefficients."""

i = 0
while(i < 304):
  print('Regressor coeffients for multiple linear regression:',clf.coef_[i])
  i = i+1