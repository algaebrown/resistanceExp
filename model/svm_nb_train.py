#import
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from multiprocessing import Pool
### import data

def txt_to_df(filename):

    path = "/home/hermuba/data/data_from_dr_wu/"
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

        train_size = math.floor(len(label)*portion)

        all_train = all_train + list(label[shuffle_index[:train_size]])
        all_test = all_test + list(label[shuffle_index[train_size:]])

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

def preprocessing(df_ris,portion):
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

    return(X_train, X_test, y_train, y_test)
def evaluate(model, X_test, y_test):
    accuracy = accuracy_score(y_test, model.predict(X_test))
    precision = precision_score(y_test, model.predict(X_test))
    f = f1_score(y_test, model.predict(X_test))
    recall = recall_score(y_test, model.predict(X_test))
    try:
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])

    except ValueError:
        auc = 0
    return([accuracy, precision, f, recall, auc])


# run naive bayes
def train_nb(df_ris, portion):
    X_train, X_test, y_train, y_test = preprocessing(df_ris, portion)
    print(sum(y_train), len(y_train))

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


    l = []
    l.append(v)
    l = l+evaluate(bnb, X_test, y_test)
    return(l)

# run svm
from sklearn import svm
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve
from sklearn.model_selection import StratifiedKFold # this is the problem!!
def train_SVM(df_ris, portion):

    X_train, X_test, y_train, y_test = preprocessing(df_ris, portion)
    # choose estimator (our model)
    clf = svm.SVC(kernel='linear', C=1, probability = True).fit(X_train, y_train)

    # cross validation
    skf = StratifiedKFold(n_splits=2, random_state=None, shuffle=False)
    cv = skf.split(X_train, y_train)

    # tune hyperparameters
    gammas = np.logspace(-6, -1, 10)
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': gammas,
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    classifier = GridSearchCV(estimator=clf, param_grid = tuned_parameters, cv = None)
    classifier.fit(X_train.values, np.asarray(y_train))
    v = classifier.cv_results_['mean_test_score'][classifier.best_index_]

    l = []
    l.append(v)
    l= l +evaluate(classifier, X_test, y_test)
    return(l)

# run a hundred times
def run_hundred(model, df, portion):
    sum_score = np.empty((0,6), int)

    for i in range(100):

        returning = model(df,portion)
        returning_for_check = np.array(returning)
        print(returning)
        if 0 not in returning_for_check[[2,3,5]]: # if no auc ValueError, precision, f score
            print('included')

            sum_score = np.append(sum_score, np.asarray([returning]), axis = 0)
        #else:
        #    print("unsucessful AUC/Precision/F score")

    std = np.std(sum_score, axis = 0)
    mean = np.mean(sum_score, axis = 0)
    print(sum_score)
    return(np.append(mean, std))

#those drugs have nearly 50 data, therefore their data are selected for training
train_drug = ['meropenem','cefepime','ceftazidime' ,'gentamicin', 'ciprofloxacin','trimethoprim_sulfamethoxazole', 'ampicillin', 'cefazolin', 'ampicillin_sulbactam', 'ceftriaxone', 'piperacillin_tazobactam', 'tobramycin']

prefix = ['card_pattern', 'gene_pattern', 'acc_pattern', 'acc_card_pattern']
portion = [0.6, 0.8]
model = [train_SVM, train_nb]

# run for all drug, portion and model


def run_drug(d):
    i = 0
    total = pd.DataFrame(columns = ['drug', 'feature', 'train_size', 'model', 'validation_accuracy', 'accuracy', 'precision', 'F1_score', 'recall', 'aur_roc','validation_accuracy_std', 'accuracy_std', 'precision_std', 'F1_score_std', 'recall_std', 'aur_roc_std'])
    for pre in prefix:
        for p in portion:
            for m in model:
                print("running", str(m), "for ", d)
                result = list(run_hundred(m, txt_to_df(pre+'.'+d), p))
                print(result)
                param = [d,pre,p,str(m)]
                total.loc[i, :] = param + result
                i +=1
    total.to_pickle("/home/hermuba/data/"+d+'_ml_df')

#if __name__=='__main__':
#with Pool(8) as p:
#    print(p.map(run_drug, ['piperacillin_tazobactam']))
