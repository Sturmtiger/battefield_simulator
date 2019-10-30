"""
Special functions for battlefield-simulator game
"""

import numpy


def geometric_mean(iterable):
    """
    :param iterable: take list of numbers
    :return: geometric mean (float type)
    """
    log_array = numpy.log(iterable)
    # print('\n\n', 'iterable:', iterable, '\n','a:', a, '\n','len(a):', len(a), '\n\n')
    return numpy.exp(log_array.sum() / len(log_array))


def unit_iterator(verification_property, *unit_iterables):
    """
    :param verification_property: property checking unit
    :param unit_iterables: take lists of units
    :return: generator of units that have passed verification_property
    """
    for unit_list in unit_iterables:
        for unit in unit_list:
            if getattr(unit, verification_property):
                yield unit
