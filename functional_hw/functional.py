import sys
import numpy as np


def sequential_map(*args):
    *functions, values = args

    for fun in functions:
        values = list(map(fun, values))

    return values


def consensus_filter(*args):
    *functions, values = args

    for fun in functions:
        values = list(filter(fun, values))

    return values


def conditional_reduce(conditional_fun, apply_fun, values):
    filtered_values = list(filter(conditional_fun, values))

    return apply_fun(filtered_values[0], filtered_values[1])


def func_chain(*functions):
    def new_funct(*values):
        for fun in functions:
            values = list(map(fun, values))
        return values

    return new_funct


def sequential_map_integrated(*args):
    *functions, values = args
    map_fun = func_chain(*functions)

    return map_fun(*values)


def multiple_partial(*functions, **arguments):
    list_of_functions = []

    def funct_factory(funct_to_change):
        def partial_fun(*args, **kwargs):
            arguments.update(kwargs)
            return funct_to_change(*args, **arguments)

        return partial_fun

    for fun in functions:
        new_fun = funct_factory(fun)
        list_of_functions.append(new_fun)

    return list_of_functions


def super_print(*args, sep=' ', end='\n', file=None):
    text = (list(map(str, args)))
    stdout = sep.join(text) + end

    if file:
        sys.stdout = open(file, 'w')
    sys.stdout.write(stdout)


if __name__ == '__main__':
    print(
        sequential_map(lambda x: x ** 3, lambda x: x ** 0.5, [1, 2, 3, 4, 5]),
        consensus_filter(lambda x: x > 3, lambda x: x < 6, [1, 2, 3, 4, 5]),
        conditional_reduce(lambda x: x > 3, lambda x, y: x * y, [1, 2, 3, 4, 5]),
        sequential_map_integrated(lambda x: x ** 3, lambda x: x ** 0.5, [1, 2, 3, 4, 5]),
        sep='\n'
    )

    my_fun = func_chain(lambda x: x + 2, lambda x: (x / 4, x // 4))
    print(my_fun(37, 4))

    ax1_mean, ax1_max, ax1_sum = multiple_partial(np.mean, np.max, np.sum, axis=1)
    ar = np.arange(6).reshape(2, 3)
    print(ar)
    print(ax1_sum(ar), ax1_max(ar), ax1_mean(ar))

    new_min, new_max = multiple_partial(min, max, key=lambda x: -x)
    print(new_max(1, 2, 2), new_min(1, 2, 3))

    super_print('What a pain, Argentina vs Jamaica:', 5, ":", 0, sep='  ', end='!')
    super_print('''He said, "One day, you'll leave this world behind
So live a life you will remember"
My father told me when I was just a child
"These are the nights that never die"''', file='Avicii.txt')
