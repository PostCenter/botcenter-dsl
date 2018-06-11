import operator as op
from collections import OrderedDict
from functools import reduce, cmp_to_key

from botlang.evaluation.values import Nil


def append(*values):
    return reduce(op.add, values)


def extend(lst, value):
    if isinstance(value, list):
        return lst + value
    return lst + [value]


def sort_function(comparator_function, lst):
    cmp_fun = lambda a, b: -1 if comparator_function(a, b) else 1
    return list(sorted(lst, key=cmp_to_key(cmp_fun)))


def find_in_list(find_function, lst):
    for elem in lst:
        if find_function(elem):
            return elem
    return Nil


def cons(head, tail):

    if isinstance(tail, list):
        return [head] + tail
    return [head, tail]


def dict_put(ordered_dict, key, value):
    return OrderedDict(
        list(ordered_dict.items()) + [(key, value)]
    )


def dict_put_mutate(ordered_dict, key, value):
    ordered_dict[key] = value
    return value


def get_or_nil(data_struct, key):
    try:
        return data_struct[key]
    except KeyError:
        return Nil
    except IndexError:
        return Nil


def dict_or_list_get(data_dict, key):
    return data_dict[key]


def dict_has_key(data_dict, key):
    try:
        return data_dict[key]
    except:
        return Nil


def make_dict(bindings):
    return OrderedDict(bindings)


COMMON_OPERATIONS = {
    'get': dict_or_list_get,
    'get-or-nil': get_or_nil,
}


DICT_OPERATIONS = {
    'make-dict': make_dict,
    'put': dict_put,
    'put!': dict_put_mutate,
    'associations': lambda d: list(d.items()),
    'keys': lambda d: list(d.keys()),
    'values': lambda d: list(d.values())
}


LIST_OPERATIONS = {
    'append': append,
    'extend': extend,
    'head': lambda x: x[0],
    'tail': lambda x: x[1:],
    'init': lambda x: x[:-1],
    'last': lambda x: x[-1],
    'length': len,
    'list': lambda *x: list(x),
    'map': lambda f, l: list(map(f, l)),
    'reduce': lambda f, l: reduce(f, l),
    'fold': lambda v, f, l: reduce(f, l, v),
    'filter': lambda f, l: list(filter(f, l)),
    'sort': sort_function,
    'max': max,
    'min': min,
    'find': find_in_list,
    'cons': cons,
    'reverse': lambda l: l[::-1],
    'enumerate': lambda l: list(enumerate(l)),
    'sum': sum
}
