from rdkit import Chem
from .fingerprinter import FingerPrinter
from pickle import dumps


def formatRecord(Compound, Targets):
    mol = Chem.MolFromSmiles(str(Compound['canonical_smiles'][0]))
    fingerprinter = FingerPrinter()
    bson_encoded = ({"CHEMBL_ID": Compound['chembl_id'][0],
                     "MOL": (dumps(mol)),
                     "FingerPrint_AtomPairs":
                     (dumps(fingerprinter.getAtomPairsFingerPrint(mol))),
                     "FingerPrint_Topological":
                     (dumps(fingerprinter.getTopologicalFingerPrint(mol))),
                     "FingerPrint_Morgan":
                     (dumps(fingerprinter.getMorganFingerPrint(mol))),
                     "Properties": {"ALOGP": Compound['alogp'][0],
                                    "PSA": Compound['psa'][0],
                                    "HBA": Compound['hba'][0],
                                    "HBD": Compound['hbd'][0],
                                    "RTB": Compound['rtb'][0]
                                    },
                     })
    bson_encoded["Targets"] = Targets
    
    return (bson_encoded)
