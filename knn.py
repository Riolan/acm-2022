import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import pandas as pd
import matplotlib.ticker as ticker
import ast
import json
import re
from database import UsersTB
from functools import reduce
import operator

data = UsersTB.access_data().fetchall()
data_ = []
for x in data:
    data_+=(reduce(operator.add, ast.literal_eval(x[3])))

def split_batches(batch_size, batch_lst):
    for i in range(0, len(batch_lst), batch_size):
        yield data_[i:i + batch_size]

real_data = list()
for batch in split_batches(3, data_):
    real_data.append(batch)


df = pd.DataFrame(real_data*6, columns=['id', 'time', 'correct'])

print(df)


X = df.drop(['correct'], axis=1)
y = df['correct']

from sklearn import preprocessing
X = preprocessing.StandardScaler().fit(X).transform(X.astype(float))

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=4)


from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
#Train Model and Predict
k = 4
neigh = KNeighborsClassifier(n_neighbors = k).fit(X_train,y_train)
Pred_y = neigh.predict(X_test)
print("Accuracy of model at K=4 is", metrics.accuracy_score(y_test, Pred_y))


error_rate = []
for i in range(1,40):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))

 
plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,color='blue', linestyle='dashed', 
         marker='o',markerfacecolor='red', markersize=10)

plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')
plt.savefig('test.png')
print("Minimum error:-",min(error_rate),"at K =",error_rate.index(min(error_rate)))


acc = []
# Will take some time
from sklearn import metrics
for i in range(1,40):
    neigh = KNeighborsClassifier(n_neighbors = i).fit(X_train,y_train)
    yhat = neigh.predict(X_test)
    acc.append(metrics.accuracy_score(y_test, yhat))
    
plt.figure(figsize=(10,6))
plt.plot(range(1,40),acc,color = 'blue',linestyle='dashed', 
         marker='o',markerfacecolor='red', markersize=10)
plt.title('accuracy vs. K Value')
plt.xlabel('K')
plt.ylabel('Accuracy')
plt.savefig('test2.png')
print("Maximum accuracy:-",max(acc),"at K =",acc.index(max(acc)))
