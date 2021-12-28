import pandas as pd
import numpy as np
from numpy import nan
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import matplotlib.patches as mpatches
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split,cross_val_score,KFold,GridSearchCV
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score, brier_score_loss,plot_roc_curve
from sklearn.model_selection import StratifiedKFold
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict




timestamp = pd.read_csv("/content/bitdata.csv", sep=",", 
                    names = ['timestamp','open','high','low','close','vol(btc)','vol(curr)','weightedprice'])
timestamp = timestamp.dropna().iloc[1: , :] # drop Nan, drop first row (title row)
timestamp.reset_index(drop=True, inplace=True)



#timestamp.sample(frac=1)
timestamp.head()



"""
Preprocessing for Bitcoin Dataset
"""

def comparator(column):
  result = [0]
  for row in range(1, len(column.index)):
    next = float(column[row])
    now = float(column[row-1])
    if next > now:
      result.append(1)
    elif next < now:
      result.append(0)
    else:
      result.append(0) # for now
    if row % 1000000 == 0: print("at " + str(row))
  return result

length = len(timestamp.index)
col_headings = ['open','low','close','vol(btc)','weightedprice','high']
for heading in col_headings:
  print("Processing " + heading)
  newCol = comparator(timestamp[heading])
  timestamp[heading] = newCol

timestamp = timestamp.drop(['timestamp','vol(curr)'],axis=1)

for column in timestamp:
    enc=LabelEncoder()
    if timestamp.dtypes[column]==np.object:
         timestamp[column]=enc.fit_transform(timestamp[column])
         
         
         
         
X = timestamp.iloc[:,:-1]
y = timestamp.iloc[:,-1]

test_size = int(len(timestamp.index) * 0.2)

X_train = X[:-test_size]
X_test = X[-test_size:]
y_train = y[:-test_size]
y_test = y[-test_size:]

timestamp.head()




dmat=xgb.DMatrix(X_train,y_train)
test_dmat=xgb.DMatrix(X_test)
final_p={'colsample_bytree':0.5, 'max_depth': 7, 'min_child_weight': 0,'subsample':  1,'reg_lambda': 1,'objective':'binary:logistic','eta': 0.1,'n_estimators':100, "silent": 1}
final_clf=xgb.train(params=final_p ,dtrain=dmat) #num_boost_round=837

xgb_pred=final_clf.predict(test_dmat)
xgb_pred[xgb_pred > 0.5 ] = 1
xgb_pred[xgb_pred <= 0.5] = 0
print(accuracy_score(y_test,xgb_pred)*100)




cm = confusion_matrix(y_test,xgb_pred)
ax= plt.subplot()
sns.heatmap(cm, annot=True, fmt='g', ax=ax);  #annot=True to annotate cells, ftm='g' to disable scientific notation

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels'); 
ax.set_title('Confusion Matrix'); 
ax.xaxis.set_ticklabels(['Decr', 'Incr']); ax.yaxis.set_ticklabels(['Decr', 'Incr']);





import graphviz

xgb.plot_importance(final_clf)

# plot the output tree via matplotlib, specifying the ordinal number of the target tree
# xgb.plot_tree(xgb_model, num_trees=xgb_model.best_iteration)

# converts the target tree to a graphviz instance
xgb.to_graphviz(final_clf)
