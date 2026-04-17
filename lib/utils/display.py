'''
Module Name : display_utils
Description : Utilities for plotting and external output display
Version     : 1.0.0
Author      : Youngkeun Kim
Created     : 2026-04-16
Updated     : 2026-04-16
Notes       : Initial version
'''

def print_mat(mat_np):
    '''
    mat_np (np.ndarray): matrix or vector you want to print on cmd.
    - 1D array: print column vector
    - 2D array: print matrix
    '''

    # 1D vector -> column vector
    if mat_np.ndim == 1:
        mat_np = mat_np.reshape(-1, 1)

    # 2D
    if mat_np.ndim != 2:
        raise ValueError("print_mat only supports 1D or 2D arrays.")

    mat = mat_np.tolist()
    mat = [[str(x) for x in row] for row in mat]
    col_widths = [max(len(row[j]) for row in mat) for j in range(len(mat[0]))]

    n_rows = len(mat)

    for i, row in enumerate(mat):
        row_str = "  ".join(f"{val:<{col_widths[j]}}" for j, val in enumerate(row))

        if n_rows == 1:
            left, right = "[", "]"
        elif i == 0:
            left, right = "[", "]"
        elif i == n_rows - 1:
            left, right = "[", "]"
        else:
            left, right = "[", "]"

        print(f"{left} {row_str} {right}")