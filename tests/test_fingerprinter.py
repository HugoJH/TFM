from drugdealer.fingerprinter import FingerPrinter

class testFingerPrintCreator():
    
    def setUp(self):
        self.sampleSMILE = "Cc1cc(ccc1C(=O)c2ccccc2Cl)N3N=CC(=O)NC3=O"
        self.sampleInchi = "OWRSAHYFSSNENM-UHFFFAOYSA-N"
        
        AtomPairsFile = open("mock/AtomPairsFingerPrint.pickle","rb")
        self.atomPairsFingerPrint = pickle.load(file=AtomPairsFile)
        AtomPairsFile.close()
        
        MorganFile = open("mock/MorganFingerPrint.pickle","rb")
        self.morganFingerPrint = pickle.load(file=MorganFile)
        MorganFile.close()
        
        TopologicalFile = open("mock/TopologicalFingerPrint.pickle","rb")
        self.topologicalFingerPrint = pickle.load(file=TopologicalFile)
        TopologicalFile.close()
        
        self.FingerPrintCreator = FingerPrinter()
    
    def test_getTopologicalFingerPrint(self):
    	pass

    def test_getMorganFingerPrint(self):
    	pass

    def test_getAtomPairsFingerPrint(self):
        pass
