from rdkit import Chem
from .fingerprinter import FingerPrinter
from pickle import dumps


def formatRecord(OneRecordDataframe):
    mol = Chem.MolFromSmiles(str(OneRecordDataframe['canonical_smiles'][0]))
    fingerprinter = FingerPrinter()
    bson_encoded = ({"CHEMBL_ID": OneRecordDataframe['chembl_id'][0],
                     "MOL": (dumps(mol)),
                     "FingerPrint_AtomPairs":
                     (dumps(fingerprinter.getAtomPairsFingerPrint(mol))),
                     "FingerPrint_Topological":
                     (dumps(fingerprinter.getTopologicalFingerPrint(mol))),
                     "FingerPrint_Morgan":
                     (dumps(fingerprinter.getMorganFingerPrint(mol))),
                     "Properties": {"ALOGP": OneRecordDataframe['alogp'][0],
                                    "PSA": OneRecordDataframe['psa'][0],
                                    "HBA": OneRecordDataframe['hba'][0],
                                    "HBD": OneRecordDataframe['hbd'][0],
                                    "RTB": OneRecordDataframe['rtb'][0]
                                    },
                     "Targets": []
                     })

    return (bson_encoded)
