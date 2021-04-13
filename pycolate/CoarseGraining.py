# TODO Make interactions possible.
from pycolate.Percolation import Percolation
import numpy as np
from scipy.ndimage import measurements
from scipy.optimize import fsolve
import scipy.ndimage as ndimage
import itertools
from sympy import solveset, S
from sympy import Symbol, Interval, lambdify
from sympy.parsing.sympy_parser import parse_expr
from sympy import N, latex

from sympy.plotting import plot

def hpercolates(config):

    (labeledConfig, a) = measurements.label(config)

    labels = np.unique(labeledConfig)

    labelsToCheck = labels[labels != 0]

    leftColumn = labeledConfig[:, 0]

    rightColumn = labeledConfig[:, -1]

    for label in labelsToCheck:

        left = label in leftColumn

        right = label in rightColumn

        if left and right:

            return True

    return False


def vpercolates(config):

    (labeledConfig, a) = measurements.label(config)

    labels = np.unique(labeledConfig)

    labelsToCheck = labels[labels != 0]

    topRow = labeledConfig[0]

    bottomRow = labeledConfig[-1]

    for label in labelsToCheck:

        bottom = label in bottomRow

        top = label in topRow

        if bottom and top:

            return True

    return False


def percolates(config):

    percolated = False

    if vpercolates(config) or hpercolates(config):

        percolated = True

    return percolated


def majority(config):

    if np.sum(config) > (config.size / 2):

        return True

    else:

        return False


def grains_connect(configurations):

    """Checks if a series of grains connect on their edges."""

    grain_size = len(configurations[0][0])
    num_of_grains = len(configurations)
    stacked_arrays = np.hstack(configurations)

    for i in range(1, num_of_grains):

        if not hpercolates(stacked_arrays[:, i * grain_size - 1 : i * grain_size + 1]):

            return False

    return True


def coarse_graining_estimate(grain_size: int, method=percolates, interactions=0):

    interactions += 1

    if grain_size <= 1 or (type(grain_size) != int):

        raise ValueError("grain_size must be an interger greater then 1.")

    generated_arrays = []
    passed_arrays = []
    amount_of_each = {}

    # There must be a faster way of generating this array?
    p = [
        np.reshape(np.array(i), (grain_size, grain_size))
        for i in itertools.product([0, 1], repeat=grain_size * grain_size)
    ]

    for configuration in p:

        if method(configuration):

            passed_arrays.append(configuration)

    if interactions > 1:

        passed_arrays = itertools.product(
            passed_arrays, repeat=interactions
        )

        temp_arrays = []

        for configurations in passed_arrays:

            if grains_connect(configurations):

                temp_arrays.append(np.hstack(configurations))

        passed_arrays = temp_arrays

    for current_array in passed_arrays:

        number_of_occupied = np.sum(current_array)

        try:
            amount_of_each[number_of_occupied] += 1
        except KeyError:
            amount_of_each[number_of_occupied] = 1

    items_in_computation = []

    for key in amount_of_each:

        tmp = "({})*(p**{})*((1-p)**{})".format(
            amount_of_each[key], key, (((grain_size) ** 2) * interactions) - key
        )

        items_in_computation.append(tmp)

        equation_to_solve = "+".join(items_in_computation)

    equation_to_solve = "(" + equation_to_solve + ")"

    if interactions > 1:

        equation_to_solve = equation_to_solve + f"**{1.0/interactions}"

    equation_to_solve = equation_to_solve + " - p"

    p = Symbol("p")

    f = lambdify(p,parse_expr(equation_to_solve))

    return fsolve(f,0.6)

    return N(solution)


if __name__ == "__main__":

    print(coarse_graining_estimate(5,interactions=1))