# Logistic Regression
from sklearn import metrics
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, RandomizedSearchCV
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

def random_forest_classification_RSCV(data_train, data_test, type_train, type_test):
    #Random forest
    param_dist = {"max_depth": [3, None],
          "max_features": ['log2'],
          "min_samples_split": sp_randint(2, 11),
          "min_samples_leaf": sp_randint(2, 11),
          "bootstrap": [True, False],
          "criterion": ["gini", "entropy"]}

    n_iter_search = 30
    random_search = RandomizedSearchCV(RandomForestClassifier(n_estimators=100), param_distributions=param_dist,
                                       n_iter=n_iter_search, n_jobs=5)

    start = time()
    random_search.fit(data_test, type_test)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))


    fitted_model = model_fit(RandomForestClassifier(**random_search.best_params_, n_estimators=888), data_train, type_train)
    predicted = model_predict(fitted_model, data_test)

    print(metrics.classification_report(type_test, predicted))
    print(metrics.confusion_matrix(type_test, predicted))

def random_forest_classification_GSCV(data_train, data_test, type_train, type_test):
    #Random forest
    param_dist = {"max_depth": [3, None],
          "max_features": sp_randint(1, 5),
          "min_samples_split": sp_randint(2, 11),
          "min_samples_leaf": sp_randint(2, 11),
          "bootstrap": [True, False],
          "criterion": ["gini", "entropy"]}

    RF_pipeline = Pipeline([('clf', RandomForestClassifier(n_estimators=10))])

    param_grid = [{'clf__n_estimators': [10,30,100],
                   'clf__max_features':[3,4,5],
                   'clf__bootstrap': [True, False],
                   'clf__criterion': ["gini", "entropy"]
                  }]

    grid_search = GridSearchCV(estimator=RF_pipeline, param_grid=param_grid,
                               scoring='f1_micro', n_jobs=5, cv=5)

    grid_search_fitted = grid_search.fit(data_train, type_train)

    print ("Finished grid search fitting...now the real deal!")
    n_iter_search = 30
    best_params = dict()
    for key, value in grid_search_fitted.best_params_.items():
        best_params[key[5:]] = value

    RF_model = RandomForestClassifier(**best_params)

    start = time()
    fitted_model = model_fit(RF_model, data_train, type_train)

    print("Model fitting took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))



    predicted = model_predict(fitted_model, data_test)

    print(metrics.classification_report(type_test, predicted))
    print(metrics.confusion_matrix(type_test, predicted))



def ANN_classification(data_train, data_test, type_train, type_test):
        clf = MLPClassifier(solver='sgd', alpha=1e-5,
                            hidden_layer_sizes=(5, 2), random_state=1)

        fitted_model = model_fit(clf,data_train, type_train)
        predicted = model_predict(fitted_model, data_test)
        print(metrics.classification_report(type_test, predicted))
        print(metrics.confusion_matrix(type_test, predicted))

def GaussNB_classification(data_train, data_test, type_train, type_test):
    print ("GaussianNB Model")
    fitted_model = model_fit(GaussianNB(), data_train, type_train)
    predicted = model_predict(fitted_model, data_test)

    print(metrics.classification_report(type_test, predicted))
    print(metrics.confusion_matrix(type_test, predicted))

"""Main module."""
if __name__ == '__main__':
    for Target in mongoDB["compounds"].distinct("Targets"):
        data_train, data_test, type_train, type_test = prepare_data(Target)

        # Logistic Regression model
#        print("Logistic Regression model")
 #       fitted_model = model_fit(LogisticRegression(n_jobs=5, max_iter=100, solver='lbfgs'), data_train, type_train)
  #      predicted = model_predict(fitted_model, data_test)


   #     print(metrics.classification_report(type_test, predicted))
    #    print(metrics.confusion_matrix(type_test, predicted))

     #   random_forest_classification_RSCV(data_train, data_test, type_train, type_test)


        random_forest_classification_GSCV(data_train, data_test, type_train, type_test)
      #  ANN_classification(data_train, data_test, type_train, type_test)


        # # # #SVM
        # from sklearn.preprocessing import MinMaxScaler
        # scaler = MinMaxScaler(feature_range=(-1,1))
        # scaler.fit(data_train)

        # normalized_data_train = scaler.transform(data_train)
        # normalized_data_test = scaler.transform(data_test)
        # svm_pipeline = Pipeline([('clf', SVC(random_state=1))])

        # param_range = [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

        # param_grid = [{'clf__C': param_range,
        #                'clf__gamma': param_range,
        #                'clf__kernel': ['rbf']
        #               },
        #               {'clf__C': param_range,
        #                'clf__degree':[2, 3, 4],
        #                'clf__kernel':['poly'],
        #               }]

        # grid_search = GridSearchCV(estimator=svm_pipeline, param_grid=param_grid,
        #                            scoring='f1_micro', n_jobs=5, cv=5)
        # grid_search_fitted = grid_search.fit(normalized_data_train, type_train)

        # print ("Finished grid search fitting...now the real deal!")
        # svm = SVC(C=grid_search.best_params_['clf__C'],
        #           cache_size=700,
        #           class_weight=grid_search_fitted.best_params_['clf__class_weight'],
        #           gamma=grid_search_fitted.best_params_['clf__gamma'],
        #           kernel=grid_search_fitted.best_params_['clf__kernel'],
        #           verbose=True)




        # print ("SVM Model")
        # fitted_model = model_fit(BaggingClassifier(svm, max_samples=0.5, max_features=0.5), data_train, type_train)
        # predicted = model_predict(fitted_model, data_test)

        # print(metrics.classification_report(type_test, predicted))
        # print(metrics.confusion_matrix(type_test, predicted))

        # #Gaussian Naïve-Bayes
        # GaussNB_classification(data_train, data_test, type_train, type_test)

        import ipdb; ipdb.set_trace()