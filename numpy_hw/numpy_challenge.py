import numpy as np


def matrix_multiplication(m1, m2):
    """
    Multiplication of two matrices by matrix multiplication rules (not elementwise) in order they were written
    sign @ is equal to numpy.matmul() method

    :param m1: first matrix
    :param m2: second matrix
    :return: result of multiplication of matrices m1 and m2
    """
    return m1 @ m2


def multiplication_check(*matrices):
    """
    Checking whether matrices can be multiplied
    The check is based on equality of number of columns of first matrix and number of rows of second matrix etc.

    :param: matrices to check
    :return: True/False in dependence on whether matrices can be multiplied
    """
    for i in range(0, len(matrices) - 1):
        if matrices[i].shape[1] != matrices[i + 1].shape[0]:
            return False
        else:
            return True


def multiply_matrices(*matrices):
    """
    Multiplication of several matrices by matrix multiplication rules (not elementwise) in order they were written

    :param matrices: matrices to multiply
    :return: result of matrices multiplication
    """
    if multiplication_check(matrices):
        return np.linalg.multi_dot(matrices)
    else:
        return


def compute_2d_distance(v1, v2):
    """
    Calculates of euclidian distance between two linear arrays (vectors) of length two

    :param v1: first linear array of length two
    :param v2: second linear array of length two
    :return: euclidian distance between arrays v1 nd v2
    """
    return np.sqrt(((v1 - v2) ** 2).sum())


def compute_multidimensional_distance(v1, v2):
    """
    Calculates of euclidian distance between two linear arrays (vectors) of same length

    :param v1: first linear array
    :param v2: second linear array
    :return: euclidian distance between arrays v1 nd v2
    """
    return np.linalg.norm(v1 - v2)


def compute_pair_distances(m):
    """
    Calculates pairwise euclidian distances between rows ob matrix and makes matrix of distances

    :param m: matrix
    :return: matrix of pairwise euclidian distances between rows ob matrix a
    """

    # make a zero square matrix with a size equal to the number of rows in matrix a
    dist_mat = np.zeros((m.shape[0], m.shape[0]))

    # pairs of row numbers of matrix m between which distances will be calculated
    # also these are coordinates of future triangular matrix of distances
    i_row, i_column = np.triu_indices(3, k=1)  # for 3x3 matrix: i_row = array(0, 0, 1); i_column = array(1, 1, 2)

    # calculating pairwise distances step by step
    differences = m[i_row] - m[i_column]  # i_row and i_column here uses as numbers of rows of matrix m
    sums_of_squares = (differences ** 2).sum(axis=1)
    distances = np.sqrt(sums_of_squares)

    # making matrix of distances
    dist_mat[i_row, i_column] = distances  # i_row and i_column here uses as coordinates of new triangular matrix
    dist_mat += dist_mat.transpose()  # making symmetric matrix

    return dist_mat


if __name__ == '__main__':
    arr1 = np.array([1, 2, 3, 4, 5, 6])  # 1 2 3 4 5 6
    arr2 = np.arange(1, 7)  # 1 2 3 4 5 6
    arr3 = np.ones(6) * 5  # 5 5 5 5 5 5
