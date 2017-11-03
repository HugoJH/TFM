# Logistic Regression
from sklearn import metrics
from sklearn.preprocessing import Normalizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from operator import itemgetter

from sklearn import preprocessing
from sklearn.pipeline import Pipeline
import numpy as np

from scipy.stats import randint as sp_randint
from time import time

from pymongo import MongoClient
mongoDB = MongoClient()["DrugDealer"]

def prepare_data(Target):

    cursor_actives = mongoDB["compounds"].find({"Targets": Target})
    actives_count = cursor_actives.count()
    cursor_decoys = mongoDB["compounds"].find({"Targets": {"$nin": [Target]}}).limit(actives_count*1)

    dataset = []

    for active in cursor_actives:
        item = [np.int(1), list(active["Properties"].values())]
        dataset.append(item)


    for decoy in cursor_decoys:
        item = [np.int(0), list(decoy["Properties"].values())]
        dataset.append(item)


    np.random.shuffle(dataset)

    type_test  = [elem[0] for elem in dataset[0:np.int(len(dataset) * 0.2)]]
    data_test  = [elem[1] for elem in dataset[0:np.int(len(dataset) * 0.2)]]
    type_train = [elem[0] for elem in dataset[np.int(len(dataset) * 0.2):]]
    data_train = [elem[1] for elem in dataset[np.int(len(dataset) * 0.2):]]
    return data_train, data_test, type_train, type_test


def model_fit(model, data, target):
    return model.fit(data, target)

def model_predict(fitted_model, test_data):
   return fitted_model.predict(test_data)

def print_prediction_results(original, predicted):
    print(metrics.classification_report(original, predicted))
    print(metrics.confusion_matrix(original, predicted))

def random_forest_classification_RSCV(data_train, data_test, type_train, type_test):
    #Random forest
    param_dist = {"max_depth": [None],
          "max_features": ['log2', None],
          "bootstrap": [True, False],
          "criterion": ["gini", "entropy"]}

    n_iter_search = 5
    random_search = RandomizedSearchCV(RandomForestClassifier(n_estimators=100), param_distributions=param_dist,
                                       n_iter=n_iter_search, n_jobs=5)

    start = time()
    random_search.fit(data_test, type_test)

    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))


    fitted_model = model_fit(RandomForestClassifier(**random_search.best_params_, n_estimators=888), data_train, type_train)
    predicted = model_predict(fitted_model, data_test)

    return predicted

def random_forest_classification_GSCV(data_train, data_test, type_train, type_test):
    #Random forest
    param_dist = {"max_depth": [None],
                  "max_features": ['log2', None],
                  "bootstrap": [True, False],
                  "criterion": ["gini", "entropy"]}

    RF_pipeline = Pipeline([('clf', RandomForestClassifier(n_estimators=10))])

    param_grid = [{'clf__n_estimators': [10,20],
                   'clf__max_features':[3,4,5],
                   'clf__bootstrap': [True, False],
                   'clf__criterion': ["gini", "entropy"]
                  }]

    grid_search = GridSearchCV(estimator=RF_pipeline, param_grid=param_grid,
                               scoring='f1_micro', n_jobs=5, cv=3)

    grid_search_fitted = grid_search.fit(data_train, type_train)



    best_params = dict()
    for key, value in grid_search_fitted.best_params_.items():
        best_params[key[5:]] = value

    RF_model = RandomForestClassifier(**best_params)

    fitted_model = model_fit(RF_model, data_train, type_train)

    predicted = model_predict(fitted_model, data_test)

    return predicted

def ANN_classification(data_train, data_test, type_train, type_test):

    print ("Artificial Neural Network")

    clf = MLPClassifier(solver='sgd', alpha=1e-5,
                        hidden_layer_sizes=(5, 2), random_state=1)

    fitted_model = model_fit(clf, data_train, type_train)
    predicted = model_predict(fitted_model, data_test)

    return predicted

def GaussNB_classification(data_train, data_test, type_train, type_test):

    print ("GaussianNB Model")

    fitted_model = model_fit(GaussianNB(), data_train, type_train)
    predicted = model_predict(fitted_model, data_test)

    return predicted

def logistic_regression_classification(data_train, data_test, type_train, type_test):

    print("Logistic Regression model")

    param_grid = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000],
                  'solver': ['newton-cg', 'saga', 'lbfgs'],
                  'max_iter': [100, 250, 1000, 4000]
                 }
    random_search = RandomizedSearchCV(LogisticRegression(), param_distributions=param_grid, n_jobs=5)

    start = time()
    fitted_model = model_fit(random_search, data_train, type_train)

    print("RandomizedSearchCV took %.2f seconds"
          " parameter settings." % ((time() - start)))


    fitted_model = model_fit(LogisticRegression(**random_search.best_params_, n_jobs=5), data_train, type_train)
    predicted = model_predict(fitted_model, data_test)
    return predicted

def test(Target):

    data_train, data_test, type_train, type_test = prepare_data(Target)

    print ("Testing for target ", Target)
    predicted_LR = logistic_regression_classification(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_LR)

    predicted_RF_RSCV = random_forest_classification_RSCV(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_RF_RSCV)

    predicted_RF_GSCV = random_forest_classification_GSCV(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_RF_GSCV)

    predicted_ANN = ANN_classification(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_ANN)

    predicted_NB = GaussNB_classification(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_NB)


def normalized_test(Target):
    print("Normalized version test")
    data_train, data_test, type_train, type_test = prepare_data(Target)

    scaler = Normalizer().fit(data_train)
    data_train = scaler.transform(data_train)
    data_test = scaler.transform(data_test)

    print ("Testing for target ", Target)
    predicted_LR = logistic_regression_classification(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_LR)

    predicted_RF_RSCV = random_forest_classification_RSCV(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_RF_RSCV)

    predicted_RF_GSCV = random_forest_classification_GSCV(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_RF_GSCV)

    predicted_ANN = ANN_classification(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_ANN)

    predicted_NB = GaussNB_classification(data_train, data_test, type_train, type_test)

    print_prediction_results(type_test, predicted_NB)
