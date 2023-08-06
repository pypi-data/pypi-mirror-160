import pickle
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# fill in your classifier in the following line:
model = XGBClassifier(n_estimators=100, max_depth=8, learning_rate=0.6, booster="gbtree", gamma=0.1, min_child_weight=0.2, reg_alpha=0.2, reg_lambda=0.5)

# fill in the name of the file in the following line:
file_name = "../../demo_files/XBGClassifier.pkl"
with open(file_name, 'wb') as file:
    pickle.dump(model, file)