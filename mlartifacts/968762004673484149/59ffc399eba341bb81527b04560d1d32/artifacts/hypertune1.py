from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
import pandas as pd
import mlflow

mlflow.set_tracking_uri('http://127.0.0.1:5000')

#load dataset
data = load_breast_cancer()
x = pd.DataFrame(data.data,columns=data.feature_names)
y = pd.Series(data.target,name='target')

#train_test_split
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size=0.10,random_state=42)

#Creating a RandomForestClassifier
rf = RandomForestClassifier(random_state=42)

#Defining the parameters grid fo GridSearchCV
param_grid = {
    'max_depth':[None,10,20,30],
    'n_estimators':[25,50,75,100]
}

#Applying the GridSearchCV
# grid_search = GridSearchCV(estimator=rf,param_grid=param_grid,cv=5,n_jobs=1,verbose=2)

# #Run wthout mlflow
# grid_search.fit(X_train,y_train)

# #Displaying the best params and best score
# best_params = grid_search.best_params_
# best_score = grid_search.best_score_

# print(best_params)
# print(best_score)

#Run with mlflow
mlflow.set_experiment('breast-cancer-rf-hp')
with mlflow.start_run():
    grid_search = GridSearchCV(estimator=rf,param_grid=param_grid,cv=5,n_jobs=1,verbose=2)
    grid_search.fit(X_train,y_train)

    #Displaying the best parameters and the best score
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    #logging the metrics
    mlflow.log_metric('accuracy',best_score)

    #logging the paarams
    mlflow.log_params(best_params)

    #log training data
    train_df = X_train.copy()
    train_df['target'] = y_train

    train_df = mlflow.data.from_pandas(train_df)
    mlflow.log_input(train_df,'training')

    #log test data
    test_df = X_test.copy()
    test_df['target'] = y_test

    test_df = mlflow.data.from_pandas(test_df)
    mlflow.log_input(test_df,'testing')

    #log the source code
    mlflow.log_artifact(__file__)

    #log the best model
    mlflow.sklearn.log_model(grid_search.best_estimator_,'random_forest')

    #Set tags
    mlflow.set_tags({'Author':'Ankit','Project':'Hypertune using MLFlow'})

    print(best_params)
    print(best_score)
