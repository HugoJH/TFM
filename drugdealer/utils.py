
def formatRecord(OneRecordDataframe):
    mol = Chem.MolFromSmiles(DFRow['canonical_smiles'])
    bson_encoded = ({"CHEMBL_ID": DFRow['chembl_id'],
                     "MOL": (dumps(mol)),
                     "FingerPrint_AtomPairs": (dumps(self.fingerprinter.getAtomPairsFingerPrint(mol))),
                     "FingerPrint_Topological": (dumps(self.fingerprinter.getTopologicalFingerPrint(mol))),
                     "FingerPrint_Morgan": (dumps(self.fingerprinter.getMorganFingerPrint(mol))),
                     "Properties": {"ALOGP": DFRow['alogp'],
                                    "PSA": DFRow['psa'],
                                    "HBA": DFRow['hba'],
                                    "HBD": DFRow['hbd'],
                                    "RTB": DFRow['rtb']
                                   },
                     "Targets": []
                    })

