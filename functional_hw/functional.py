import sys


def sequential_map(*args):
    """
    sequential_map takes several functions, and container of values to which these functions will be applied
    and return list of results after application all functions to values container.

    [!] Functions should return application results of them.
    [!] Container of values should always be written last.
    [!] Functions apply in order that they were written.

    :param args: functions and container of values (last!).
    :return: list with modified values from container.
    """

    *functions, values = args

    for fun in functions:
        values = list(map(fun, values))

    return values


def consensus_filter(*args):
    """
    consensus_filter takes several filtering functions, and container of values to which these functions will be applied
    and return list of values that passed application of functions to them with returning True.

    [!] Functions should return True/False.
    [!] Container of values should always be written last.
    [!] Functions apply in order that they were written.

    :param args: functions and container of values (last!).
    :return: list with values from container which passed the filtration.
    """

    *functions, values = args

    for fun in functions:
        values = list(filter(fun, values))

    return values


def conditional_reduce(conditional_fun, apply_fun, values):
    """
    conditional_reduce takes values that filters with special function (conditional_fun)
    and then applies another function (apply_fun) to values passed by the filter.
    apply_fun is applied cumulatively in given order to the values (like base reduce function)

    [!] If container with values has length of one, conditional_reduce will return the first value of container
    [!] At least one value should pass the filter.
    If only one value have been passed, conditional_reduce will return it.

    :param conditional_fun: filtering function.
    :param apply_fun: function that is applied to values passed the filtering cumulatively in given order.
    :param values: container of values.
    :return: result of application [apply_fun] to filtered by [conditional_fun] values from container [values].
    """
    filtered_values = list(filter(conditional_fun, values))

    if not filtered_values:
        raise IndexError("list with values passed by the filter has zero length")

    result = filtered_values[0]
    for next_val in filtered_values[1:]:
        result = apply_fun(result, next_val)

    return result


def func_chain(*args):
    """
    func_chain takes functions and return one new function that includes all taken functions.
    This new function applies all taken functions in the given order to given values.

    [!] Functions apply in order that they were written.
    [!] Functions should return application results of them.

    New function takes some values (*values)
    and returns list of modified values or one value (not listed) depended on number of values in result.

    :param args: functions.
    :return: new function includes taken functions.
    """

    def new_funct(*values):
        for fun in args:
            values = list(map(fun, values))
        if len(values) == 1:
            return values[0]
        return values

    return new_funct


def sequential_map_2(*args):
    """
    [This function have the same functionality as sequential_map, but utilizes func_chain function in it.]

    sequential_map_2 takes several functions, and container of values to which these functions will be applied
    and return list of results after application all functions to values container.

    [!] Functions should return application results of them.
    [!] Container of values should always be written last.
    [!] Functions apply in order that they were written.

    :param args: functions and container of values (last!).
    :return: list with modified values from container.
    """

    *functions, values = args
    map_fun = func_chain(*functions)

    return map_fun(*values)


def multiple_partial(*functions, **params):
    """
    multiple_partial takes functions (*functions) and modifies them with setting their parameters (*params) by default.

    multiple_partial includes func_factory function to create new independent functions with set parameters.

    [!] If some modified function is used with new parameters which differ from set with multiple_partial,
    modified function will use new parameters.

    :param functions: functions to modify.
    :param params: parameters to set default.
    :return: list of modified functions.
    """

    def func_factory(funct_to_change):
        def partial_fun(*args, **kwargs):
            params.update(kwargs)
            return funct_to_change(*args, **params)

        return partial_fun

    list_of_functions = []

    for fun in functions:
        new_fun = func_factory(fun)
        list_of_functions.append(new_fun)

    return list_of_functions


def super_print(*args, sep=' ', end='\n', file=None):
    """
    [The FULL COPY of base print function]

    Prints the values to a stream, or to sys.stdout by default.

    :param args: values to print.
    :param sep: string inserted between values, default a space.
    :param end: string appended after the last value, default a newline.
    :param file: a file to write to.
    :return: None
    """

    text = (list(map(str, args)))
    stdout = sep.join(text) + end

    if file:
        sys.stdout = open(file, 'w')
    sys.stdout.write(stdout)


if __name__ == '__main__':
    # SOME TESTING

    assert sequential_map(lambda x: x ** 2, lambda x: x + 1, [1, 2, 3, 4, 5]) == [2, 5, 10, 17, 26]
    assert sequential_map(lambda x: x + " wow", lambda x: x[-3:], ['abc', 'efg']) == ['wow', 'wow']

    assert consensus_filter(lambda x: x > 3, lambda x: x < 6, [1, 2, 3, 4, 5]) == [4, 5]
    assert consensus_filter(lambda x: len(x) > 3, lambda x: x[-1] == '!', ['wow!', 'how?', 'ok!']) == ['wow!']

    assert conditional_reduce(lambda x: x > 2, lambda x, y: x * y, [1, 2, 3, 4, 5]) == 60
    assert conditional_reduce(lambda x: len(x) > 3 and x[-1] == '!',
                              lambda x, y: x + ' ' + y,
                              ['wow!', 'how!', 'ok!', 'thanks!']) == "wow! how! thanks!"
    assert conditional_reduce(lambda x: x > 2, lambda x: x ** 2, [3]) == 3

    assert sequential_map_2(lambda x: x ** 2, lambda x: x + 1, [1, 2, 3, 4, 5]) == [2, 5, 10, 17, 26]
    assert sequential_map(lambda x: x + " wow", lambda x: x.upper(), ['one', 'two']) == ['ONE WOW', 'TWO WOW']

    my_fun = func_chain(lambda x: x + 2, lambda x: (x / 4, x // 4))
    assert my_fun(37) == (9.75, 9)
    assert my_fun(7, 17) == [(2.25, 2), (4.75, 4)]

    new_min, new_max = multiple_partial(min, max, key=lambda x: -x)
    assert new_max(1, 2, 3), new_min(1, 2, 3) == (1, 3)
    assert new_max(1, 2, 3, key=lambda x: x), new_min(1, 2, 3, key=lambda x: x) == (3, 1)

    # What a pain, Argentina vs Jamaica:	5	:	0 !
    super_print('What a pain, Argentina vs Jamaica:', 5, ":", 0, sep='\t', end=' !')

    # You can see result file in repository
    super_print('He said, "One day, you\'ll leave this world behind', 'So live a life you will remember"',
                'My father told me when I was just a child', '"These are the nights that never die"',
                sep='\n', file='Avicii.txt')
