from rdkit.Chem.Fingerprints.FingerprintMols import FingerprintMol as TopologicalFingerPrint 
from rdkit.Chem.AllChem import GetMorganFingerprint as MorganFingerPrint 
from rdkit.Chem.AtomPairs.Pairs import GetAtomPairFingerprint as AtomPairFingerPrint

class FingerPrinter:

    def __init__(self):
        pass

    def getAtomPairsFingerPrint(self, mol):
        pass
 
    def getMorganFingerPrint(self, mol):      
        pass

    def getTopologicalFingerPrint(self, mol):      
        pass