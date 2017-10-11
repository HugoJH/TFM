from pymongo import MongoClient
from .utils import formatRecord
from psycopg2 import connect
from pathlib import Path
from os.path import join, dirname
from pandas import read_sql

class DBPopulator:

    def __init__(self):
        self.client = MongoClient()
        self.mongoDB = self.client['DrugDealer']
        #self.SQLiteDB = connect(str(Path(join(dirname(__file__),
        #    "../DBs/chembl_22_1.db")).resolve()))
        self.con = connect(dbname="chembl_23", user="postgres", password="postgres")
        self.chunksize = 1000
        self.preparing_tables_query = """
        DROP TABLE IF EXISTS COMPOUNDS_TARGETS;
        CREATE TABLE COMPOUNDS_TARGETS AS
        SELECT MOLREGNO, COMPOUND, TARGET, ORGANISM
        FROM (
            SELECT MD.MOLREGNO, MD.CHEMBL_ID as COMPOUND, TD.CHEMBL_ID as TARGET, TD.ORGANISM, COUNT(1) OVER (PARTITION BY TD.CHEMBL_ID) AS cnt
            FROM (((MOLECULE_DICTIONARY MD
            INNER JOIN ACTIVITIES AC ON (MD.MOLREGNO = AC.MOLREGNO))
            INNER JOIN ASSAYS ASS ON (AC.ASSAY_ID = ASS.ASSAY_ID))
            INNER JOIN (SELECT * FROM TARGET_DICTIONARY WHERE ORGANISM in ('Homo sapiens', 'Mus musculus', 'Rattus norvegicus')) AS TD ON (ASS.TID = TD.TID))
        ) as v
        WHERE cnt > 20
        GROUP BY MOLREGNO, COMPOUND, TARGET, ORGANISM;
        ALTER TABLE COMPOUNDS_TARGETS ADD CONSTRAINT PK_COMPOUNDS_TARGETS PRIMARY KEY (COMPOUND, TARGET);
        CREATE INDEX IDX_CT_MOLREGNO ON public.compounds_targets USING btree (molregno ASC NULLS LAST) TABLESPACE pg_default;
        CREATE INDEX IDX_CT_MOLREGNO_COMPOUND ON public.compounds_targets USING btree (molregno ASC NULLS LAST, COMPOUND ASC NULLS LAST) TABLESPACE pg_default;

        DROP TABLE IF EXISTS FILTERED_COMPOUND_PROPERTIES;

        CREATE TABLE FILTERED_COMPOUND_PROPERTIES AS
        SELECT COMPOUND, alogp, hba, hbd, psa, rtb, canonical_smiles
                FROM (SELECT DISTINCT MOLREGNO, COMPOUND FROM COMPOUNDS_TARGETS )  CT
                    inner join compound_structures on (CT.MOLREGNO = compound_structures.molregno)
                    inner join compound_properties on (compound_structures.molregno = compound_properties.molregno)
        where
        compound_properties.alogp IS NOT NULL
        AND compound_properties.hba IS NOT NULL
        AND compound_properties.hbd IS NOT NULL
        AND compound_properties.psa IS NOT NULL
        AND compound_properties.rtb IS NOT NULL
        AND compound_structures.canonical_smiles IS NOT NULL;

        COMMIT;
        """


        self.targets_query = """ SELECT TARGET, ORGANISM FROM COMPOUNDS_TARGETS WHERE COMPOUND = '%s' """

        self.compound_properties_query = """ SELECT * FROM FILTERED_COMPOUND_PROPERTIES """

    def targets_from_compound(self, compound_id):
        return (read_sql(sql=self.targets_query % (compound_id), con=self.con)["target"].values.tolist())

    def prepareTables(self):
        self.cur = self.con.cursor()
        self.cur.execute(self.preparing_tables_query)

    def populateDatabase(self):
        documents = []

        i = 0
        for results in read_sql(sql=self.compound_properties_query,
                               con=self.con,
                               chunksize=self.chunksize):
            try:
                for _, row in results.iterrows():
                    targets = self.targets_from_compound(row['compound'])
                    record = formatRecord(row, targets)
                    documents.append(record)

                self.mongoDB['compounds'].insert_many(documents)
                del documents
                documents = []
                print("Conjunto"+ str(i) + "volcado en mongoDB" )
                i += 1
            except:
                pass
        if documents:
            self.mongoDB['compounds'].insert_many(documents)
