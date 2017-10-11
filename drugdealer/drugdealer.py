# -*- coding: utf-8 -*-
from fingerprinter import FingerPrinter
from computesimilarity import ComputeSimilarity
from pymongo import MongoClient
from pickle import loads

def demo_calculo_similitud():

    db = MongoClient()['DrugDealer']["compounds"]
    threshold = 0.75
    similarity = ComputeSimilarity()
    sample_molecule = db.find().limit(2444)[1123]
    sample_molecule_fingerprint = sample_molecule["FingerPrints"]["AtomPairs"]["data"]
    print(type(sample_molecule_fingerprint))
    for molecule in db.find():
        try:
            tanimoto = similarity.getTanimotoSimilarity(loads(sample_molecule_fingerprint), loads(molecule["FingerPrints"]["AtomPairs"]["data"]))
            if tanimoto > threshold:
                print ('%s : %s' % (tanimoto, molecule['CHEMBL_ID']))
        except:
            pass

"""Main module."""
if __name__ == '__main__':
    demo_calculo_similitud()