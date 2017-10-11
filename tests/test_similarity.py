
import pickle
from drugdealer.computesimilarity import ComputeSimilarity
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
from pathlib import Path
from os.path import join, dirname


class TestSimilarity:

    def test_getTanimotoSimilarity(self):
        self.ComputeSimilarity = ComputeSimilarity()
        self.sampleSMILE1 = "Cc1cc(ccc1C(=O)c2ccccc2Cl)N3N=CC(=O)NC3=O"
        self.sampleSMILE2 = "BP(=O)(OP(=O)(O)OP(=O)(O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N2C=CC(=O)NC2=O)OP(=O)(O)OP(=O)(O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)N4C=CC(=O)NC4=O.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC"
        fingerprint1File = open(str(Path(join(dirname(__file__),
                            "mock/MorganFingerPrint1.pickle"))
                            .resolve()), "rb")
        fingerprint2File = open(str(Path(join(dirname(__file__),
                           "mock/MorganFingerPrint2.pickle"))
                           .resolve()), "rb")

        self.fingerprint1 = pickle.load(file=fingerprint1File)
        self.fingerprint2 = pickle.load(file=fingerprint2File)
        fingerprint1File.close()
        fingerprint2File.close()
        self.tanimotoSimilarity =  0.0601092
        similarity = self.ComputeSimilarity.getTanimotoSimilarity(self.fingerprint1,self.fingerprint2)
        assert abs(similarity - self.tanimotoSimilarity) < 0.0001

    def test_getDiceSimilarity(self):
        self.ComputeSimilarity = ComputeSimilarity()
        self.sampleSMILE1 = "Cc1cc(ccc1C(=O)c2ccccc2Cl)N3N=CC(=O)NC3=O"
        self.sampleSMILE2 = "BP(=O)(OP(=O)(O)OP(=O)(O)OC[C@H]1O[C@H]([C@H](O)[C@@H]1O)N2C=CC(=O)NC2=O)OP(=O)(O)OP(=O)(O)OC[C@H]3O[C@H]([C@H](O)[C@@H]3O)N4C=CC(=O)NC4=O.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC.CCCCN(CCCC)CCCC"
        fingerprint1File = open(str(Path(join(dirname(__file__),
                            "mock/MorganFingerPrint1.pickle"))
                            .resolve()), "rb")
        fingerprint2File = open(str(Path(join(dirname(__file__),
                           "mock/MorganFingerPrint2.pickle"))
                           .resolve()), "rb")

        self.fingerprint1 = pickle.load(file=fingerprint1File)
        self.fingerprint2 = pickle.load(file=fingerprint2File)
        fingerprint1File.close()
        fingerprint2File.close()
        self.diceSimilarity = 0.1134020
        similarity = self.ComputeSimilarity.getDiceSimilarity(self.fingerprint1,self.fingerprint2)
        assert abs(similarity - self.diceSimilarity) < 0.0001
