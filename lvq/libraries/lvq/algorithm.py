from __future__ import division

import numpy as np
from copy import deepcopy

from neupy import init
from neupy.utils import format_data
from neupy.exceptions import NotTrained
from neupy.algorithms.base import BaseNetwork
from neupy.core.properties import (IntProperty, Property, TypedListProperty,
                                   NumberProperty)


__all__ = ('LVQ', 'LVQ2', 'LVQ21', 'LVQ3')


def euclid_distance(input_data, weight):
    """
    Negative Euclidian distance between input
    data and weight.

    Parameters
    ----------
    input_data : array-like
        Input data.

    weight : array-like
        Neural network's weights.

    Returns
    -------
    array-like
    """
    input_data = np.expand_dims(input_data, axis=0)
    euclid_dist = np.linalg.norm(input_data - weight, axis=1)
    return np.expand_dims(euclid_dist, axis=0)


def n_argmin(array, n, axis=0):
    """
    Returns indeces of n minimum values.

    Parameters
    ----------
    array : array-like

    n : int
        Number of minimum indeces.

    axis : int
        Axis along which to search minimum values.
        Defaults to ``0``.

    Returns
    -------
    array-like
    """
    sorted_argumets = array.argsort(axis=axis).ravel()
    return sorted_argumets[:n]


class LVQ(BaseNetwork):
    """
    Learning Vector Quantization (LVQ) algorithm.

    Notes
    -----
    - Input data needs to be normalized, because LVQ uses
      Euclidian distance to find clusters.

    - Training error is just a ratio of miscassified
      samples

    Parameters
    ----------
    n_inputs : int
        Number of input units. It should be equal to the
        number of features in the input data set.

    n_subclasses : int, None
        Defines total number of subclasses. Values should be greater
        or equal to the number of classes. ``None`` will set up number
        of subclasses equal to the number of classes. Defaults to ``None``
        (or the same as ``n_classes``).

    n_classes : int
        Number of classes in the data set.

    prototypes_per_class : list, None
        Defines number of prototypes per each class. For instance,
        if ``n_classes=3`` and ``n_subclasses=8`` then there are
        can be 3 subclasses for the first class, 3 for the second one
        and 2 for the third one (3 + 3 + 2 == 8). The following example
        can be specified as ``prototypes_per_class=[3, 3, 2]``.

        There are two rules that apply to this parameter:

        1. ``sum(prototypes_per_class) == n_subclasses``

        2. ``len(prototypes_per_class) == n_classes``

        The ``None`` value will distribute approximately equal
        number of subclasses per each class. It's approximately,
        because in casses when ``n_subclasses % n_classes != 0``
        there is no way to distribute equal number of subclasses
        per each class.

        Defaults to ``None``.

    {BaseNetwork.step}

    n_updates_to_stepdrop : int or None
        If this options is not equal to ``None`` then after every
        update LVQ reduces step size and do it until number of
        applied updates would reach the ``n_updates_to_stepdrop``
        value. The minimum possible step size defined in the
        ``minstep`` parameter.

        Be aware that number of updates is not the same as number
        of epochs. LVQ applies update after each propagated sample
        through the network. Relations between this parameter and
        maximum number of epochs is following

        .. code-block:: python

            n_updates_to_stepdrop = n_samples * n_max_epochs

        If parameter equal to ``None`` then step size wouldn't be
        reduced after each update.

        Defaults to ``None``.

    minstep : float
        Step size would never be lower than this value. This
        property useful only in case if ``n_updates_to_stepdrop``
        is not ``None``. Defaults to ``1e-5``.

    {BaseNetwork.show_epoch}

    {BaseNetwork.shuffle_data}

    {BaseNetwork.epoch_end_signal}

    {BaseNetwork.train_end_signal}

    {Verbose.verbose}

    Methods
    -------
    {BaseSkeleton.predict}

    {BaseSkeleton.fit}
    """
    n_inputs = IntProperty(minval=1)
    n_subclasses = IntProperty(minval=2, default=None, allow_none=True)
    n_classes = IntProperty(minval=2)

    prototypes_per_class = TypedListProperty(allow_none=True, default=None)
    weight = Property(expected_type=(np.ndarray, init.Initializer),
                      allow_none=True, default=None)

    n_updates_to_stepdrop = IntProperty(default=None, allow_none=True,
                                        minval=1)
    minstep = NumberProperty(minval=0, default=1e-5)

    pengurangan_step = NumberProperty(minval=0, default=0)

    def __init__(self, **options):
        self.initialized = False
        super(LVQ, self).__init__(**options)

        self.n_updates = 0

        if self.n_subclasses is None:
            self.n_subclasses = self.n_classes

        if isinstance(self.weight, init.Initializer):
            weight_shape = (self.n_inputs, self.n_subclasses)
            self.weight = self.weight.sample(weight_shape)

        if self.weight is not None:
            self.initialized = True

        if self.n_subclasses < self.n_classes:
            raise ValueError("Number of subclasses should be greater "
                             "or equal to the number of classes. Network "
                             "was defined with {} subclasses and {} classes"
                             "".format(self.n_subclasses, self.n_classes))

        if self.prototypes_per_class is None:
            whole, reminder = divmod(self.n_subclasses, self.n_classes)
            self.prototypes_per_class = [whole] * self.n_classes

            if reminder:
                # Since we have reminder left, it means that we cannot
                # have an equal number of subclasses per each class,
                # therefor we will add +1 to randomly selected class.
                class_indeces = np.random.choice(self.n_classes, reminder,
                                                 replace=False)

                for class_index in class_indeces:
                    self.prototypes_per_class[class_index] += 1

        if len(self.prototypes_per_class) != self.n_classes:
            raise ValueError("LVQ defined for classification problem that has "
                             "{} classes, but the `prototypes_per_class` "
                             "variable has defined data for {} classes."
                             "".format(self.n_classes,
                                       len(self.prototypes_per_class)))

        if sum(self.prototypes_per_class) != self.n_subclasses:
            raise ValueError("Invalid distribution of subclasses for the "
                             "`prototypes_per_class` variable. Got total "
                             "of {} subclasses ({}) instead of {} expected"
                             "".format(sum(self.prototypes_per_class),
                                       self.prototypes_per_class,
                                       self.n_subclasses))

        self.subclass_to_class = []
        for class_id, n_prototypes in enumerate(self.prototypes_per_class):
            self.subclass_to_class.extend([class_id] * n_prototypes)

    @property
    def training_step(self):
        if self.n_updates_to_stepdrop is None:
            return self.step

        updates_ratio = (1 - self.n_updates / self.n_updates_to_stepdrop)
        return self.minstep + (self.step - self.minstep) * updates_ratio

    #method tambahan
    def update_learning_rate(self):
        if (self.pengurangan_step == 0):
            return self.step

        step_baru = self.step - self.pengurangan_step
        if (step_baru > self.minstep):
            self.step = step_baru

        return self.step

    def predict(self, input_data):
        if not self.initialized:
            raise NotTrained("LVQ network hasn't been trained yet")

        input_data = format_data(input_data)
        subclass_to_class = self.subclass_to_class
        weight = self.weight

        predictions = []
        for input_row in input_data:
            output = euclid_distance(input_row, weight)
            winner_subclass = int(output.argmin(axis=1))

            predicted_class = subclass_to_class[winner_subclass]
            predictions.append(predicted_class)

        return np.array(predictions)

    def train(self, input_train, target_train, *args, **kwargs):
        input_train = format_data(input_train)
        target_train = format_data(target_train)

        n_input_samples = len(input_train)

        if n_input_samples <= self.n_subclasses:
            raise ValueError("Number of training input samples should be "
                             "greater than number of sublcasses. Training "
                             "method recived {} input samples."
                             "".format(n_input_samples))

        if not self.initialized:
            target_classes = sorted(np.unique(target_train).astype(np.int))
            expected_classes = list(range(self.n_classes))

            if target_classes != expected_classes:
                raise ValueError("All classes should be integers from the "
                                 "range [0, {}], but got the following "
                                 "classes instead {}".format(
                                    self.n_classes - 1, target_classes))

            weights = []
            indeces = []
            iterator = zip(target_classes, self.prototypes_per_class)
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

            self.weight = np.array(weights)
            self.initial_weight = deepcopy(self.weight)
            self.indeces = indeces
            self.initialized = True

        super(LVQ, self).train(input_train, target_train, *args, **kwargs)

    def train_epoch(self, input_train, target_train):
        weight = self.weight
        subclass_to_class = self.subclass_to_class

        n_correct_predictions = 0
        for input_row, target in zip(input_train, target_train):
            step = self.training_step
            output = euclid_distance(input_row, weight)
            winner_subclass = int(output.argmin())
            predicted_class = subclass_to_class[winner_subclass]

            weight_update = input_row - weight[winner_subclass, :]
            is_correct_prediction = (predicted_class == target)

            if is_correct_prediction:
                weight[winner_subclass, :] += step * weight_update
            else:
                weight[winner_subclass, :] -= step * weight_update

            n_correct_predictions += is_correct_prediction
            self.n_updates += 1

        n_samples = len(input_train)
        return 1 - n_correct_predictions / n_samples


class LVQ2(LVQ):
    """
    Learning Vector Quantization 2 (LVQ2) algorithm.
    Improved version for the LVQ algorithm.

    Parameters
    ----------
    epsilon : float
        Ration between to closest subclasses that
        triggers double weight update. Defaults to ``0.1``.

    {LVQ.Parameters}

    Notes
    -----
    {LVQ.Notes}
    """
    epsilon = NumberProperty(default=0.1)

    def train_epoch(self, input_train, target_train):
        weight = self.weight
        epsilon = self.epsilon
        subclass_to_class = self.subclass_to_class

        n_correct_predictions = 0
        for input_row, target in zip(input_train, target_train):
            step = self.training_step
            output = euclid_distance(input_row, weight)
            winner_subclasses = n_argmin(output, n=2, axis=1)

            top1_subclass, top2_subclass = winner_subclasses
            top1_class = subclass_to_class[top1_subclass]
            top2_class = subclass_to_class[top2_subclass]

            top1_weight_update = input_row - weight[top1_subclass, :]
            is_correct_prediction = (top1_class == target)

            closest_dist, runner_up_dist = output[0, winner_subclasses]
            double_update_condition_satisfied = (
                not is_correct_prediction and
                (top2_class == target) and
                closest_dist > ((1 - epsilon) * runner_up_dist) and
                runner_up_dist < ((1 + epsilon) * closest_dist)
            )

            if double_update_condition_satisfied:
                top2_weight_update = input_row - weight[top2_class, :]
                weight[top1_subclass, :] -= step * top1_weight_update
                weight[top2_subclass, :] += step * top2_weight_update

            elif is_correct_prediction:
                weight[top1_subclass, :] += step * top1_weight_update

            else:
                weight[top1_subclass, :] -= step * top1_weight_update

            n_correct_predictions += is_correct_prediction

        self.update_learning_rate()
        print("LVQ 2 Learning Rate: {}".format(self.step))
        n_samples = len(input_train)
        return 1 - n_correct_predictions / n_samples


class LVQ21(LVQ2):
    """
    Learning Vector Quantization 2.1 (LVQ2.1) algorithm.
    Improved version for the LVQ2 algorithm.

    Parameters
    ----------
    {LVQ2.Parameters}

    Notes
    -----
    {LVQ2.Notes}
    """
    def train_epoch(self, input_train, target_train):
        weight = self.weight
        epsilon = self.epsilon
        subclass_to_class = self.subclass_to_class

        n_correct_predictions = 0
        for input_row, target in zip(input_train, target_train):
            step = self.training_step
            output = euclid_distance(input_row, weight)
            winner_subclasses = n_argmin(output, n=2, axis=1)

            top1_subclass, top2_subclass = winner_subclasses
            top1_class = subclass_to_class[top1_subclass]
            top2_class = subclass_to_class[top2_subclass]

            top1_weight_update = input_row - weight[top1_subclass, :]
            is_correct_prediction = (top1_class == target)

            closest_dist, runner_up_dist = output[0, winner_subclasses]
            double_update_condition_satisfied = (
                (
                    (top1_class == target and top2_class != target) or
                    (top1_class != target and top2_class == target)
                ) and
                closest_dist > ((1 - epsilon) * runner_up_dist) and
                runner_up_dist < ((1 + epsilon) * closest_dist)
            )

            if double_update_condition_satisfied:
                top2_weight_update = input_row - weight[top2_class, :]

                if is_correct_prediction:
                    weight[top2_subclass, :] -= step * top2_weight_update
                    weight[top1_subclass, :] += step * top1_weight_update
                else:
                    weight[top1_subclass, :] -= step * top1_weight_update
                    weight[top2_subclass, :] += step * top2_weight_update

            elif is_correct_prediction:
                weight[top1_subclass, :] += step * top1_weight_update

            else:
                weight[top1_subclass, :] -= step * top1_weight_update

            n_correct_predictions += is_correct_prediction
            self.n_updates += 1

        self.update_learning_rate()
        print("LVQ 2.1 Learning Rate: {}".format(self.step))

        n_samples = len(input_train)
        return 1 - n_correct_predictions / n_samples


class LVQ3(LVQ21):
    """
    Learning Vector Quantization 3 (LVQ3) algorithm.
    Improved version for the LVQ2.1 algorithm.

    Parameters
    ----------
    {LVQ.n_inputs}

    {LVQ.n_subclasses}

    {LVQ.n_classes}

    {LVQ.prototypes_per_class}

    {LVQ2.epsilon}

    slowdown_rate : float
        Paremeter scales learning step in order to decrease it
        in case if the two closest subclasses predict target
        value correctly. Defaults to ``0.4``.

    step : float
        Learning rate, defaults to ``0.01``.

    {BaseNetwork.show_epoch}

    {BaseNetwork.shuffle_data}

    {BaseNetwork.epoch_end_signal}

    {BaseNetwork.train_end_signal}

    {Verbose.verbose}

    Notes
    -----
    {LVQ21.Notes}
    - Decreasing step and increasing number of training epochs
      can improve the performance.
    """
    step = NumberProperty(minval=0, default=0.01)
    slowdown_rate = NumberProperty(minval=0, default=0.4)

    def train_epoch(self, input_train, target_train):
        weight = self.weight
        epsilon = self.epsilon
        slowdown_rate = self.slowdown_rate
        subclass_to_class = self.subclass_to_class

        n_correct_predictions = 0
        for input_row, target in zip(input_train, target_train):
            step = self.training_step
            output = euclid_distance(input_row, weight)
            winner_subclasses = n_argmin(output, n=2, axis=1)

            top1_subclass, top2_subclass = winner_subclasses
            top1_class = subclass_to_class[top1_subclass]
            top2_class = subclass_to_class[top2_subclass]

            top1_weight_update = input_row - weight[top1_subclass, :]
            is_first_correct = (top1_class == target)
            is_second_correct = (top2_class == target)

            closest_dist, runner_up_dist = output[0, winner_subclasses]
            double_update_condition_satisfied = (
                (
                    (is_first_correct and not is_second_correct) or
                    (is_second_correct and not is_first_correct)
                ) and
                closest_dist > ((1 - epsilon) * runner_up_dist) and
                runner_up_dist < ((1 + epsilon) * closest_dist)
            )
            two_closest_correct_condition_satisfied = (
                is_first_correct and is_second_correct and
                closest_dist > ((1 - epsilon) * (1 + epsilon) * runner_up_dist)
            )

            if double_update_condition_satisfied:
                top2_weight_update = input_row - weight[top2_class, :]

                if is_first_correct:
                    weight[top1_subclass, :] += step * top1_weight_update
                    weight[top2_subclass, :] -= step * top2_weight_update
                else:
                    weight[top1_subclass, :] -= step * top1_weight_update
                    weight[top2_subclass, :] += step * top2_weight_update

            elif two_closest_correct_condition_satisfied:
                beta = step * slowdown_rate
                top2_weight_update = input_row - weight[top2_class, :]

                weight[top1_subclass, :] += beta * top1_weight_update
                weight[top2_subclass, :] += beta * top2_weight_update

            else:
                weight[top1_subclass, :] -= step * top1_weight_update

            n_correct_predictions += is_first_correct
            self.n_updates += 1

        n_samples = len(input_train)
        return 1 - n_correct_predictions / n_samples
