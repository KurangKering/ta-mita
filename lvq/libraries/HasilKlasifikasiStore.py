class HasilKlasifikasiSaver:
    def __init__(self, model):
        self.model = model


    def getMetode(self):
        metode = self.model.getMetode()
        return metode

    def getEpochs(self):
        epochs = self.epochs
        return epochs

    def getLR(self):
        lr = self.learning_rate
        return lr

    def getMinimumLR(self):
        min_lr = self.minimum_lr
        return min_lr

    def getPenguranganLR(self):
        pengurangan_lr = self.pengurangan_lr
        return pengurangan_lr

    def getPersenUji(self):
        persen_uji = self.persen_uji
        return persen_uji

    def getDataLatih(self):
        data_latih = self.data_latih
        return data_latih

    def getDataUji(self):
        data_uji = self.data_uji
        return data_uji

    def getTotalDataLatih(self):
        total_dl = self.total_data_latih
        return self.total_dl

    def getTotalDataUji(self):
        total_du = self.total_data_uji
        return total_du

    def getInitialWeights(self):
        initial_weights = self.initial_weights
        return initial_weights

    def getHasilKlasifikasi(self):
        result = self.hasil_klasifikasi
        return result

    def storeData(self):
        pass

    def getPath(self):
        pass
