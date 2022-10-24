import numpy as np


def matrix_multiplication(a, b):
    return a @ b


def multiplication_check(a, b):
    return a.shape[1] == b.shape[0]


def multiply_matrices(*args):
    return np.linalg.multi_dot(args)


def compute_2d_distance(a, b):
    return np.sqrt(((a - b) ** 2).sum())


def compute_multidimensional_distance(a, b):
    return np.linalg.norm(a - b)


def compute_pair_distances(a):
    dist_mat = np.zeros((a.shape[0], a.shape[0]))

    row, column = np.triu_indices(3, k=1)

    differences = a[row] - a[column]
    sums_of_squares = (differences ** 2).sum(axis=1)
    distances = np.sqrt(sums_of_squares)

    dist_mat[row, column] = distances
    dist_mat += dist_mat.transpose()

    return dist_mat


if __name__ == '__main__':
    arr1 = np.array([1, 2, 3, 4, 5, 6])
    arr2 = np.arange(1, 7)
    arr3 = np.ones(6)
