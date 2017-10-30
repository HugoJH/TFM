from rdkit import Chem
from .fingerprinter import FingerPrinter
from pickle import dumps


def formatRecord(Compound, Targets):
    mol = Chem.MolFromSmiles(Compound['canonical_smiles'])
    if mol is not None:

      fingerprinter = FingerPrinter()
      bson_encoded = ({"CHEMBL_ID": Compound['compound'],
                       "MOL": (dumps(mol)),
                       "FingerPrints": {"Morgan": {"data": dumps(fingerprinter.getMorganFingerPrint(mol)),
                                                   "length": len(dumps(fingerprinter.getMorganFingerPrint(mol)))
                                                   },
                                        "AtomPairs": {"data": dumps(fingerprinter.getAtomPairsFingerPrint(mol)),
                                                      "length": len(dumps(fingerprinter.getAtomPairsFingerPrint(mol)))
                                                      },
                                        "Topological": {"data": dumps(fingerprinter.getTopologicalFingerPrint(mol)),
                                                        "length": len(dumps(fingerprinter.getTopologicalFingerPrint(mol)))
                                                        }
                                       },
                       "Properties": {"ALOGP": Compound['alogp'],
                                      "PSA": Compound['psa'],
                                      "HBA": Compound['hba'],
                                      "HBD": Compound['hbd'],
                                      "RTB": Compound['rtb']
                                      }
                       })

    bson_encoded["Targets"] = Targets
    return (bson_encoded)
