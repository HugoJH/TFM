from pymongo import MongoClient
from .utils import formatRecord
from sqlite3 import connect
from pathlib import Path
from os.path import join, dirname
from pandas import read_sql

class DBPopulator:

    def __init__(self):
        self.client = MongoClient()
        self.mongoDB = self.client['DrugDealer']
        self.SQLiteDB = connect(str(Path(join(dirname(__file__),
                            "../DBs/chembl_22_1.db")).resolve()))
        self.compounds_query = """  
        SELECT distinct chembl_id, entity_type, alogp, hba, hbd, psa, rtb, canonical_smiles
        FROM chembl_id_lookup  inner join compound_structures 
        on (entity_type='COMPOUND' and entity_id = compound_structures.molregno)
        inner join compound_properties 
        on (compound_structures.molregno = compound_properties.molregno AND compound_properties.alogp IS NOT NULL  
        AND compound_properties.hba IS NOT NULL  
        AND compound_properties.hbd IS NOT NULL  
        AND compound_properties.psa IS NOT NULL  
        AND compound_properties.rtb IS NOT NULL)
        """
        self.targets_query = """
        SELECT distinct MD.CHEMBL_ID AS COMPOUND, TD.CHEMBL_ID as TARGET
        FROM ((((COMPOUND_STRUCTURES CS 
        INNER JOIN MOLECULE_DICTIONARY MD ON (CS.MOLREGNO = MD.MOLREGNO))
        INNER JOIN ACTIVITIES AC ON (MD.MOLREGNO = AC.MOLREGNO))
        INNER JOIN ASSAYS ASS ON (AC.ASSAY_ID = ASS.ASSAY_ID))
        INNER JOIN TARGET_DICTIONARY TD ON (ASS.TID = TD.TID)) WHERE MD.CHEMBL_ID = \"%s\"
        """                           

    def targets_from_compound(self, compound_id):
        pass
    def populateDatabase(self):
        pass


