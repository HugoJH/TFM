from sqlite3 import connect
from pathlib import Path
from pandas import read_sql
from drugdealer.utils import formatRecord
from os.path import join,dirname

def test_formatRecord():
    pathToDB = str(Path(join(dirname(__file__),"../DBs/chembl_22_1.db")).resolve())
    pathToSampleMongoRecord = str(Path(join(dirname(__file__), "mock/sampleMongoRecord.json")).resolve()) 
    print (pathToDB)
    con = connect(pathToDB)

    sql_test_query = """ SELECT distinct chembl_id, entity_type, alogp, hba, hbd, psa, rtb, canonical_smiles
                              FROM chembl_id_lookup  inner join compound_structures 
                              on (entity_type='COMPOUND' and entity_id = compound_structures.molregno)
                              inner join compound_properties 
                              on (compound_structures.molregno = compound_properties.molregno AND compound_properties.alogp IS NOT NULL  
                              AND compound_properties.hba IS NOT NULL  
                              AND compound_properties.hbd IS NOT NULL  
                              AND compound_properties.psa IS NOT NULL  
                              AND compound_properties.rtb IS NOT NULL) limit 1
                     """
    dataframeWithOneRecord = read_sql(sql=sql_test_query, con=con)
    assert formatRecord(dataframeWithOneRecord) == open(pathToSampleMongoRecord,'r').read()


