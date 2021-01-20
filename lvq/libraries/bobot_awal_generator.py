from .lvq import algorithm
import numpy as np
from neupy.utils import format_data
def bobot_awal_generator(input_train, target_train):
    np.random.seed(0)
    input_train = format_data(input_train)
    target_train = format_data(target_train)


    n_classes = np.unique(target_train).size
    n_input_samples = len(input_train)
    whole, reminder = divmod(n_classes, n_classes)
    prototypes_per_class = [whole] * n_classes

    target_classes = sorted(np.unique(target_train).astype(np.int))

    weights = []
    indeces = []
    iterator = zip(target_classes, prototypes_per_class)
    for target_class, n_prototypes in iterator:
        is_valid_class = (target_train[:, 0] == target_class)
        is_valid_class = is_valid_class.astype('float64')
        n_samples_per_class = sum(is_valid_class)
        is_valid_class /= n_samples_per_class

        if n_samples_per_class <= n_prototypes:
            raise ValueError("Input data has {0} samples for class-{1}"
                             ". Number of samples per specified "
                             "class-{1} should be greater than {2}."
                             "".format(n_samples_per_class,
                                       target_class, n_prototypes))

        class_weight_indeces = np.random.choice(
            np.arange(n_input_samples), n_prototypes,
            replace=False, p=is_valid_class)

        class_weight = input_train[class_weight_indeces]
        weights.extend(class_weight)
        indeces.append(class_weight_indeces)

    initial_weights = weights
    indeces = np.array(indeces).flatten()
    return indeces, initial_weights
