from rdkit.Chem.Fingerprints.FingerprintMols \
    import FingerprintMol as TopologicalFingerPrint
from rdkit.Chem.AllChem \
    import GetMorganFingerprint as MorganFingerPrint
from rdkit.Chem.AtomPairs.Pairs \
    import GetAtomPairFingerprint as AtomPairFingerPrint


class FingerPrinter:

    def __init__(self):
        pass

    def getAtomPairsFingerPrint(self, mol):
        try:
            fingerprint = AtomPairFingerPrint(mol)
            return fingerprint
        except Exception as e:
            print("The mol argument is not a rdkit Mol object")

    def getMorganFingerPrint(self, mol):
        try:
            fingerprint = MorganFingerPrint(mol, 2)
            return fingerprint
        except Exception as e:
            print("The mol argument is not a rdkit Mol object")

    def getTopologicalFingerPrint(self, mol):
        try:
            fingerprint = TopologicalFingerPrint(mol)
            return fingerprint
        except Exception as e:
            print("The mol argument is not a rdkit Mol object")
