from sqlite3 import connect
from pathlib import Path
from pandas import read_sql
from drugdealer.utils import formatRecord
from os.path import join, dirname
from pickle import load


def test_formatRecord():
    pathToDB = str(Path(join(dirname(__file__),
                             "../DBs/chembl_22_1.db")).resolve())
    pathToSampleMongoRecord = str(Path(join(dirname(__file__),
                                       "mock/sampleMongoRecord.json"))
                                  .resolve())

    con = connect(pathToDB)

    sql_test_query = \
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
    dataframeWithOneRecord = read_sql(sql=sql_test_query, con=con)

    sampleMongoRecordFile = open(pathToSampleMongoRecord, "rb")
    mongoRecord = load(sampleMongoRecordFile)
    sampleMongoRecordFile.close()

    assert formatRecord(dataframeWithOneRecord) == mongoRecord
