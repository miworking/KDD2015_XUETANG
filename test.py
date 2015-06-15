from sklearn.cross_validation import cross_val_score
from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier

X,y = make_blobs(n_samples=100,n_features=3,centers=10,random_state=0)

clf = DecisionTreeClassifier(max_depth=None,min_samples_split=1,random_state=0)
scores = cross_val_score(clf,X,y)
