import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine
from sklearn.metrics._plot.confusion_matrix import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

mlflow.set_tracking_uri('http://127.0.0.1:5000')

#load wine dataset
wine = load_wine()
x = wine.data
y = wine.target

#train test split
X_train,X_test,y_train,y_test = train_test_split(x,y,test_size=0.10,random_state=42)

#Define the params for model
max_depth = 15
n_estimators = 20

with mlflow.start_run():
    rf = RandomForestClassifier(max_depth=max_depth,n_estimators=n_estimators,random_state=42)
    rf.fit(X_train,y_train)

    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test,y_pred)

    mlflow.log_metric('accuracy',accuracy)
    mlflow.log_param('max_depth',max_depth)
    mlflow.log_param('n_estimators',n_estimators)

    #Creating a confusion matrix plot
    cm = confusion_matrix(y_test,y_pred)
    plt.figure(figsize=(6,6))
    sns.heatmap(cm,annot=True,fmt='d',cmap='Blues',xticklabels=wine.target_names,yticklabels=wine.target_names)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')

    #Save plt
    plt.savefig('Confusion-matrix.png')

    #log_artifacts using mlflow
    mlflow.log_artifact('Confusion-matrix.png')
    mlflow.log_artifact(__file__)

    print(accuracy)