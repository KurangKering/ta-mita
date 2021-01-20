from .lvq.algorithm import LVQ2


class MyLVQ2(LVQ2):

    def getEpochs(self):
        return self.epochs