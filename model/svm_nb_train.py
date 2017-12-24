#import
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

### import data

def txt_to_df(filename):

    path = "/home/hermuba/res/data/data_from_dr_wu/"
    i = 0
    with open(path + filename) as f:
        for line in f:
            l = line.replace('\n', '').split('\t')
            if i == 0:
                l[0] = "Genome ID"
                l[1] = "Resistant Phenotype"
                df = pd.DataFrame(columns = l)

            else:
                ID = l[0]

                df.loc[i-1, :] = l
            i += 1
    return(df)
# homemade random stratified split
def random_split(df, portion):
    positive = df.loc[df['Resistant Phenotype'] == "Resistant"].index
    negative = df.loc[df['Resistant Phenotype'] == "Susceptible"].index
    all_train = []
    all_test = []
    for label in [positive, negative]:

        arr = np.arange(len(label))
        np.random.shuffle(arr)
        shuffle_index = arr
        train_size = round(len(label)*portion)

        all_train = all_train + list(shuffle_index[:train_size])
        all_test = all_test + list(shuffle_index[train_size:])
    return(all_train, all_test)


# change to binary
to_binary={'Resistant': 1,
          'Susceptible': 0}

# throw into naive bayes
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import *
def train_nb(df_ris, portion):

    # hold out test set
    train_index, test_index = random_split(df_ris, portion)
    X = df_ris.drop(["Genome ID", "Resistant Phenotype"], axis = 1)
    y = df_ris['Resistant Phenotype'].map(to_binary)
    X_train = X.loc[train_index, :]
    X_test = X.loc[test_index, :]
    y_train = y[train_index]
    y_test = y[test_index]
    X_train.reset_index(inplace = True, drop = True)
    y_train.reset_index(inplace = True, drop = True)

    # seperate train and test into k fold
    n=10
    cv = ShuffleSplit(n_splits=n, test_size=0.3, random_state = 0)


    # bnb.fit
    bnb = BernoulliNB()
    val_score = 0
    for train_index, test_index in cv.split(X_train, y_train):
        bnb.fit(X_train.iloc[train_index,:], y_train[train_index])
        val = bnb.predict(X_train.iloc[test_index])
        score = accuracy_score(y_train[test_index], val)
        val_score = val_score + score

    v = val_score/n

    # model.predict()

    accuracy = accuracy_score(y_test, bnb.predict(X_test))
    precision = precision_score(y_test, bnb.predict(X_test))
    f = f1_score(y_test, bnb.predict(X_test))
    recall = recall_score(y_test, bnb.predict(X_test))
    auc = roc_auc_score(y_test, bnb.predict_proba(X_test))
    return([v,accuracy, precision, f, recall, auc])

# run svm
from sklearn import svm
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve
from sklearn.model_selection import StratifiedKFold # this is the problem!!


def train_SVM(df_ris, portion):

    # split test, train
    train_index, test_index = random_split(df_ris, portion)
    X = df_ris.drop(["Genome ID", "Resistant Phenotype"], axis = 1)
    y = df_ris['Resistant Phenotype'].map(to_binary)
    X_train = X.loc[train_index, :]
    X_test = X.loc[test_index, :]
    y_train = y[train_index]
    y_test = y[test_index]

    # choose estimator (our model)
    clf = svm.SVC(kernel='linear', C=1, probability = True).fit(X_train, y_train)

    # cross validation
    skf = StratifiedKFold(n_splits=3, random_state=None, shuffle=False)
    cv = skf.split(X_train, y_train)

    # tune hyperparameters
    gammas = np.logspace(-6, -1, 10)
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': gammas,
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    classifier = GridSearchCV(estimator=clf, param_grid = tuned_parameters, cv = cv)
    classifier.fit(X_train.values, np.asarray(y_train))
    v = classifier.cv_results_['mean_test_score'][classifier.best_index_]


    # returning model evaluation
    accuracy = accuracy_score(y_test, classifier.predict(X_test))
    precision = precision_score(y_test, classifier.predict(X_test))
    f = f1_score(y_test, classifier.predict(X_test))
    recall = recall_score(y_test, classifier.predict(X_test))

    auc = roc_auc_score(y_test, classifier.predict_proba(X_test)[:,1])

    return([v,accuracy, precision, f, recall, auc])

# run a hundred times
def run_hundred(model, df, portion):
    sum_score = np.zeros(6)
    for i in range(100):
        scoring_matrix = np.asarray(model(df, portion))
        sum_score = sum_score + scoring_matrix
    return(sum_score/100)

#those drugs have nearly 50 data, therefore their data are selected for training
train_drug = ['meropenem','cefepime','ceftazidime' ,'gentamicin', 'ciprofloxacin',
              'trimethoprim_sulfamethoxazole', 'ampicillin', 'cefazolin', 'ampicillin_sulbactam']

prefix = ['card_pattern', 'gene_pattern', 'acc_pattern', 'acc_card_pattern']
portion = [0.6, 0.8]
model = [train_SVM, train_nb]

# run for all drug, portion and model
total = pd.DataFrame(columns = ['drug', 'feature', 'train_size', 'model', 'validation_accuracy', 'accuracy', 'precision', 'F1_score', 'recall', 'aur_roc'])
i = 0
for d in train_drug:
    for pre in prefix:
        for p in portion:
            for m in model:
                result = list(run_hundred(m, txt_to_df(pre+'.'+d), p))
                param = [d,pre,p,str(m)]
                total.loc[i, :] = param + result
                i +=1
