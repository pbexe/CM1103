# -*- coding: utf-8 -*-

""" The various implementations for questions 1 and 2.

To run the code for question 2, run the file. To run the code for question 1,
import and run the corresponding modules from an external python
script/interpreter.
"""

import csv
import math
import random

import matplotlib.pyplot as plt
import numpy as np


def nextTime(mean):
    """ Generates a random time

    The values that this function return form a normal distribution around the
    `mean`.

    Args:
        mean (float): The mean of the random times generated

    Returns:
        float: A random time
    """
    return -mean * math.log(1 - random.random())


def theoreticalMeanQueueLength(alpha, beta):
    """ Theoretically simulates a queue

    Using the formula `(beta / alpha) / (1 - (beta / alpha))`, a theoretical
    mean queue length can be determined for various values of `alpha` and
    `beta`.

    Args:
        alpha (float): The mean time between customers entering the bank
        beta (float): The mean time of interaction between the teller and a
                      customer

    Returns:
        float: The theoretical mean queue length

    >>> theoreticalMeanQueueLength(10, 2)
    0.25
    >>> theoreticalMeanQueueLength(5, 1)
    0.25
    >>> theoreticalMeanQueueLength(4, 2)
    1.0
    >>> theoreticalMeanQueueLength(5.5, 1.3)
    0.3095238095238095
    >>> theoreticalMeanQueueLength(5.5, 0)
    0.0
    >>> theoreticalMeanQueueLength(1, 1)
    -1
    >>> type(theoreticalMeanQueueLength(10, 2))
    <class 'float'>
    """
    try:
        return (beta / alpha) / (1 - (beta / alpha))
    except ZeroDivisionError:
        return -1


def checkMean(mean, iterations=10000):
    """Checks to see whether `nextTime()` is returning values that have a mean
    of `mean`.

    Args:
        mean (float): The mean supplied to `nextTime()`
        iterations (int): The number of iteration used to generate the mean

    Returns:
        float: The actual mean on `nextTime()`

    >>> random.seed(57)
    >>> checkMean(5, 10)
    6.309113224728108
    >>> random.seed(57)
    >>> checkMean(5, 1000)
    4.973347344130324
    >>> random.seed(57)
    >>> checkMean(5, 100000)
    4.988076126529703
    >>> random.seed(57)
    >>> checkMean(195, 100000)
    194.53496893466047
    >>> random.seed(57)
    >>> checkMean(195)
    196.71853828860912
    >>> random.seed(57)
    >>> checkMean(31)
    31.273203522804728
    >>> type(checkMean(31, 5))
    <class 'float'>
    """
    total = 0
    """int: Counter used to store the running total of the returned values
    from `nextTime()`. It is divided by `iterations` to calculate the mean
    value of `nextTime()`.
    """
    for _ in range(0, iterations):
        total += nextTime(mean)
    total /= iterations
    return total


def readExperimentParameters(filename):
    """
    >>> readExperimentParameters('experiments.csv')[0]
    (10, 2, 480)
    >>> len(readExperimentParameters('experiments.csv'))
    5
    >>> readExperimentParameters('experiments.csv')[3]
    (20, 2, 480)
    >>> readExperimentParameters('experiments.csv')[2]
    (20, 15, 240)
    >>> type(readExperimentParameters('experiments.csv')[1])
    <class 'tuple'>
    """
    with open(filename, newline='') as file:
        data = list(csv.reader(file, delimiter=',', skipinitialspace=True))
        output = []
        for row in data[1:]:
            if row[3] == 'h':
                output.append((int(row[0]), int(row[1]), int(row[2]) * 60))
            else:
                output.append((int(row[0]), int(row[1]), int(row[2])))
    return output


def singleQueue(alpha, beta, time=480):
    """
    >>> random.seed(57)
    >>> singleQueue(10, 3, 480)
    3
    >>> random.seed(101)
    >>> singleQueue(5, 3, 480)
    6
    >>> random.seed(101)
    >>> singleQueue(5, 3)
    6
    >>> random.seed(935)
    >>> singleQueue(10, 9, 280)
    10
    >>> type(singleQueue(10, 9, 280))
    <class 'int'>
    """
    ta, ts, c, maxQ = 0, 0, 0, 0
    Q = 1
    simTime = time
    while True:
        if c < simTime:
            if ta < ts:
                ts -= ta
                while True:
                    c += ta
                    Q += 1
                    if Q > maxQ:
                        maxQ = Q
                    ta = nextTime(alpha)
                    if Q != 0:
                        break
            else:
                ta -= ts
                c += ts
                Q -= 1
                ts = nextTime(beta)
                while Q == 0:
                    c += ta
                    Q += 1
                    if Q > maxQ:
                        maxQ = Q
                    ta = nextTime(alpha)
        else:
            return maxQ

if __name__ == "__main__":
    alpha = np.arange(1.1, 10.1, 0.01)
    y = []
    for i in alpha:
        y.append(theoreticalMeanQueueLength(i, 1))
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.xlabel(r'$\frac{\beta}{\alpha}$', fontsize=16)
    plt.ylabel('Theoretical Mean Queue Length')
    plt.plot(alpha,y)
    plt.show()
