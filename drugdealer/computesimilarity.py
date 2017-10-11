from rdkit.DataStructs import TanimotoSimilarity, DiceSimilarity


class ComputeSimilarity:

    def __init__(self):
        pass

    def getTanimotoSimilarity(self, fingerprint1, fingerprint2):
        return TanimotoSimilarity(fingerprint1, fingerprint2)

    def getDiceSimilarity(self, fingerprint1, fingerprint2):
        return DiceSimilarity(fingerprint1, fingerprint2)
