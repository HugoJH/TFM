from sqlite3 import connect
from pathlib import Path
from pandas import read_sql
from drugdealer.utils import formatRecord
from drugdealer.DBPopulator import DBPopulator
from os.path import join, dirname
from pickle import load


def test_formatRecord():
    pathToDB = str(Path(join(dirname(__file__),
                             "../DBs/chembl_22_1.db")).resolve())
    pathToSampleMongoRecord = str(Path(join(dirname(__file__),
                                            "mock/sampleMongoRecord.bson"))
                                  .resolve())

    con = connect(pathToDB)

    compound_query = \
        """ SELECT DISTINCT chembl_id, entity_type, alogp,
                            hba, hbd, psa, rtb, canonical_smiles
            FROM chembl_id_lookup INNER JOIN compound_structures
            ON (entity_type='COMPOUND'
            AND entity_id = compound_structures.molregno)
            INNER JOIN compound_properties
            ON ( compound_structures.molregno = compound_properties.molregno
            AND compound_properties.alogp IS NOT NULL
            AND compound_properties.hba IS NOT NULL
            AND compound_properties.hbd IS NOT NULL
            AND compound_properties.psa IS NOT NULL
            AND compound_properties.rtb IS NOT NULL) LIMIT 1
        """

    targets_query = \
        """ SELECT distinct MD.CHEMBL_ID AS COMPOUND, TD.CHEMBL_ID as TARGET
            FROM ((((COMPOUND_STRUCTURES CS
            INNER JOIN MOLECULE_DICTIONARY MD ON (CS.MOLREGNO = MD.MOLREGNO))
            INNER JOIN ACTIVITIES AC ON (MD.MOLREGNO = AC.MOLREGNO))
            INNER JOIN ASSAYS ASS ON (AC.ASSAY_ID = ASS.ASSAY_ID))
            INNER JOIN TARGET_DICTIONARY TD ON (ASS.TID = TD.TID)) WHERE MD.CHEMBL_ID = \"%s\"
        """

    compound_query_result = read_sql(sql=compound_query, con=con)
    chembl_id = compound_query_result['chembl_id'][0]
    targets = read_sql(sql=targets_query % (chembl_id), con=con)["TARGET"].values.tolist()

    sampleMongoRecordFile = open(pathToSampleMongoRecord, "rb")
    mongoRecord = load(sampleMongoRecordFile)
    sampleMongoRecordFile.close()


    assert formatRecord(compound_query_result.iloc[0,:].to_dict(), targets) == mongoRecord

def test_targets_from_compound():
    db_populator = DBPopulator()
    compound_id = "CHEMBL1"
    pathToSampleTargetsList = str(Path(join(dirname(__file__),
                                            "mock/sampleTargetsList"))
                                  .resolve())

    SampleTargetsListFile = open(pathToSampleTargetsList, "rb")
    targets_list = load(SampleTargetsListFile)
    SampleTargetsListFile.close()

    assert db_populator.targets_from_compound(compound_id) == targets_list