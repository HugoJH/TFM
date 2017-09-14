from drugdealer.fingerprinter import FingerPrinter
from rdkit.Chem import MolFromSmiles
import pytest 
from pathlib import Path
from os.path import join,dirname
import pickle

class TestFingerprinter:

    def test_getTopologicalFingerPrint(self):
        fingerprinter = FingerPrinter()
        sampleSMILE = "Cc1cc(ccc1C(=O)c2ccccc2Cl)N3N=CC(=O)NC3=O"

        topologicalFile = open(str(Path(join(dirname(__file__), "mock/TopologicalFingerPrint.pickle")).resolve()), "rb")
        topologicalFingerPrint = pickle.load(file=topologicalFile)
        topologicalFile.close()

        fingerprint = fingerprinter.getTopologicalFingerPrint(mol=MolFromSmiles(sampleSMILE))
        assert fingerprint == topologicalFingerPrint

    def test_getMorganFingerPrint(self):
        fingerprinter = FingerPrinter()
        sampleSMILE = "Cc1cc(ccc1C(=O)c2ccccc2Cl)N3N=CC(=O)NC3=O"

        morganFile = open(str(Path(join(dirname(__file__), "mock/MorganFingerPrint.pickle")).resolve()), "rb")
        morganFingerPrint = pickle.load(file=morganFile)
        morganFile.close()

        fingerprint = fingerprinter.getMorganFingerPrint(mol=MolFromSmiles(sampleSMILE))
        assert fingerprint == morganFingerPrint

    def test_getAtomPairsFingerPrint(self):
        fingerprinter = FingerPrinter()
        sampleSMILE = "Cc1cc(ccc1C(=O)c2ccccc2Cl)N3N=CC(=O)NC3=O"
        
        AtomPairsFile = open(str(Path(join(dirname(__file__),"mock/AtomPairsFingerPrint.pickle")).resolve()), "rb")
        atomPairsFingerPrint = pickle.load(file=AtomPairsFile)
        AtomPairsFile.close()

        fingerprint = fingerprinter.getAtomPairsFingerPrint(mol=MolFromSmiles(sampleSMILE))
        assert fingerprint == atomPairsFingerPrint
