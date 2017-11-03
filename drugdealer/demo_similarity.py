# -*- coding: utf-8 -*-
from fingerprinter import FingerPrinter
from computesimilarity import ComputeSimilarity
from pymongo import MongoClient
from pickle import loads

def demo_calculo_similitud():

    db = MongoClient()['DrugDealer']["compounds"]
    threshold = 0.70
    similarity = ComputeSimilarity()
    sample_molecule = db.find().limit(2444)[12]
    print ("Compuesto de muestra: ",sample_molecule["CHEMBL_ID"])
    sample_molecule_fingerprint = sample_molecule["FingerPrints"]["AtomPairs"]["data"]
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
