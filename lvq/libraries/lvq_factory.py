from .lvq import algorithm
import numpy as np
np.random.seed(0)

def proses_pelatihan_lvq2(X, y, X_train, y_train, epochs, **options):

    np.random.seed(0)
    lvqnet2 = algorithm.LVQ2(
        n_inputs=X.shape[1], n_classes=np.unique(y).size, verbose=False, **options)

    lvqnet2.train(X_train, y_train, epochs=int(epochs))

    return lvqnet2


def proses_pelatihan_lvq21(X, y, X_train, y_train, epochs, **options):
    
    np.random.seed(0)
    lvqnet21 = algorithm.LVQ21(n_inputs=X.shape[1], n_classes=np.unique(y).size, 
        verbose=False, **options)

    lvqnet21.train(X_train, y_train, epochs=int(epochs))
    
    return lvqnet21 