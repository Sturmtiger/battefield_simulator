import numpy


def geometric_mean(iterable):
    a = numpy.log(iterable)
    # print('\n\n', 'iterable:', iterable, '\n','a:', a, '\n','len(a):', len(a), '\n\n')
    return numpy.exp(a.sum() / len(a))


def unit_iterator(verification_property, *unit_iterables):
    for it in unit_iterables:
        for unit in it:
            if getattr(unit, verification_property):
                yield unit
