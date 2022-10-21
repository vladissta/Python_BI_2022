import numpy as np


def matrix_multiplication(a, b):
    return a @ b


def multiplication_check(a, b):
    return a.shape[1] == b.shape[0]


def multiply_matrices(*args):
    return np.linalg.multi_dot(args)


def compute_2d_distance(a, b):
    return np.sqrt(((a - b) ** 2).sum())


def compute_multidimensional_distance():
    return np.linalg.norm(a - b)


def compute_pair_distances():
    pass


if __name__ == '__main__':
    arr1 = np.array([1, 2, 3, 4, 5, 6])
    arr2 = np.arange(1, 7)
    arr3 = (np.ones(6) + np.arange(0, 6)).astype('int')  # убери

    a = arr1.reshape(2, 3)
    b = arr1.reshape(3, 2)
    c = np.arange(1, 3)
    v1 = np.array([1, 1])
    v2 = np.array([0, 0])

    print(
        multiplication_check(a, b),
        matrix_multiplication(a, b),
        multiply_matrices(a, b, c),
        compute_2d_distance(v1, v2),
        sep='\n'
    )
