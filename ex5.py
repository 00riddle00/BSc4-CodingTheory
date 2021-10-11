
# ====================================
# Helper functions
# ====================================

def transpose(M):
    return [[M[i][j] for i in range(len(M))] for j in range(len(M[0]))]

def negative(M):
    return [[(-1 * M[i][j]) % q  for j in range(len(M[0]))] for i in range(len(M))]

def concat(M,N):
    return [M[i] + N[i] for i in range(len(M))]

def mult(M,N):
    result = [[0 for j in range(len(N[0]))] for i in range(len(M))]

    for i in range(len(M)):
        for j in range(len(N[0])):
            for l in range(len(N)):
                result[i][j] = (result[i][j] + M[i][l] * N[l][j]) % q

    return result

def subtract_vectors(u,v):
    return [(u[i] - v[i]) % q for i in range(len(u))]

# ====================================
# Main
# ====================================

text_abc = ['A', 'B', 'C', 'Č', 'D', 'E', 'Ė', 'F', 'G',
            'H', 'I', 'Y', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'R', 'S', 'Š', 'T', 'U', 'V', 'Z', 'Ž']

n = 7
q = 3
k = 2
k_zeroes = [[0 for i in range(k)]]

# '*' - deletion error
# if there is a '*', at max there can be only one distortion error in that word
# otherwise up to two distortion errors are possible
words_received_1 = \
    [[2, 2, 1, 2, 0, 1, 1],
     [1, 1, 0, 1, 0, 1, 2],
     [1, 2, 1, 1, 1, 1, 0],
     [2, 2, 2, 2, 0, 0, 1],
     ['*', 1, 0, 1, 0, 2, 2],
     [0, 0, 1, 0, '*', 0, 0],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 2, 1, 1, 1, '*', 0],
     [1, 1, 0, 1, 0, 1, 2],
     [1, 0, 2, 2, 1, '*', 2],
     [0, 2, 2, 0, 2, 0, 2],
     [2, 1, 0, 0, 1, '*', 1],
     [1, 2, 2, 0, 2, 2, 2],
     [1, 0, 1, 2, 1, 0, 2],
     [0, 0, 0, '*', 0, 0, 0],
     [1, 1, 2, 1, 2, 0, 1],
     [2, '*', 2, 1, 2, 0, 1],
     [0, 0, 0, 0, 0, 0, 0]]

# these words contain ONLY deletion errors
words_received_2 = \
    [[2, '*', '*', 2, 0, 2, '*'],
     [0, '*', 1, 1, '*', 2, '*'],
     [1, '*', 1, 2, '*', '*', 2],
     [1, '*', 1, 2, '*', '*', 2],
     [2, '*', 1, 0, 1, '*', '*'],
     ['*', 1, '*', 2, 2, 1, 0],
     [1, 2, '*', 0, '*', '*', 2],
     [1, '*', 2, '*', 2, '*', 2],
     ['*', 1, '*', 0, '*', 1, 1],
     ['*', 0, 1, 2, '*', '*', 2],
     [2, 0, '*', 1, 2, 0, '*'],
     [0, 0, '*', '*', '*', 0, 0],
     [1, '*', 1, 2, '*', '*', 2],
     [1, 0, 1, 2, 1, '*', '*'],
     [0, '*', 0, 0, 0, 0, '*']]

# matrix size: k x n = 2 x 7
G = [[1, 0, 1, 2, 1, 0, 2],
     [0, 1, 2, 2, 2, 1, 0]]

# matrix size: k x (n-k) = 2 x 5
A = [[G[0][2], G[0][3], G[0][4], G[0][5], G[0][6]],
     [G[1][2], G[1][3], G[1][4], G[1][5], G[1][6]]]

# G' = (A|I), matrix size of I: k x k = 2 x 2
I_first = [[1, 0],
           [0, 1]]

# matrix size: (n-k) x k = 5 x 2
A_T = transpose(A)

# matrix size: 5 x 2
minus_A_T = negative(A_T)

# H = (-A_T|I), matrix size of I: (n-k) x (n-k) = 5 x 5
I_second = [[1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1]]

# matrix size: (n-k) x n = 5 x 7
H = concat(minus_A_T, I_second)

# matrix size: n x (n-k) = 7 x 5
H_T = transpose(H)
