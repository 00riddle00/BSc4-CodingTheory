
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

# convert zs - lists of 2 elems -> to lists of 3 elems
def conv_list_2_to_3(zs):
    flat_zs = [item for sublist in zs for item in sublist]
    return [flat_zs[i:i + n] for i in range(0, len(flat_zs), 3)]

def print_xs():
    for x in xs:
        letter_index = x[0] + x[1] * 3 + x[2] * 9
        print(text_abc[letter_index], end='')
    print()

# ====================================
# Main
# ====================================

text_abc = ['A', 'B', 'C', 'Č', 'D', 'E', 'Ė', 'F', 'G',
            'H', 'I', 'Y', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'R', 'S', 'Š', 'T', 'U', 'V', 'Z', 'Ž']

n = 7
q = 3
k = 2
n_minus_k_zeroes = [0] * (n-k)

# '*' - deletion error (max 1 in one word)
#
# if there is a '*', at max there can be
# only 1 distortion error in that word
#
# otherwise up to 2 distortion errors are possible
#
words_received_part_1 = \
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

# these words contain ONLY deletion errors (max 3 in one word)
words_received_part_2 = \
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

# =====================
# Part 1
# =====================

words_corrected = []
xs = []

e_i_control_bits = []

for i in range(n-k):
    e_i_first = n_minus_k_zeroes[:]
    e_i_second = n_minus_k_zeroes[:]

    e_i_first[i] = 1
    e_i_second[i] = 2

    e_i_control_bits.append(e_i_first)
    e_i_control_bits.append(e_i_second)

e_i_we_care = []

# e_i_we_care will now contain those error words which have 1 error
# in info bits and 1 error in control bits
# (we don't care when both errors occur in control bits)
for error_in_info_bits in [[0,1],[0,2],[1,0],[2,0]]:
    for error_in_control_bits in e_i_control_bits:
        e_i_we_care.append(error_in_info_bits + error_in_control_bits)

# add the cases when 2 errors occur in info bits
e_i_we_care.append([1,1,0,0,0,0,0])
e_i_we_care.append([1,2,0,0,0,0,0])
e_i_we_care.append([2,1,0,0,0,0,0])
e_i_we_care.append([2,2,0,0,0,0,0])

s_i_we_care = mult(e_i_we_care,H_T)

for y in words_received_part_1:

    # if there is a '*', at max there can be only
    # 1 distortion error in that word
    if '*' in y:
        # we replace '*' with 0,1,2 (trying all possible scenarios)
        star_index = y.index('*')
        y0 = y[:]
        y1 = y[:]
        y2 = y[:]

        y0[star_index] = 0
        y1[star_index] = 1
        y2[star_index] = 2

        ys = [y0, y1, y2]

        for y in ys:
            x = y

            y = [y]
            s = mult(y,H_T)

            if s == [n_minus_k_zeroes]:
                break
            else:
                s = s[0]
                y = y[0]

                if s in s_i_we_care:
                    s_i_index = s_i_we_care.index(s)
                    e_i = e_i_we_care[s_i_index]

                    x = subtract_vectors(y,e_i)
                    break

    else:
        # x = y if the word is correct OR if the
        # error(s) was/were not in the info symbol
        x = y

        y = [y]
        s = mult(y,H_T)

        if s != [n_minus_k_zeroes]:
            s = s[0]
            y = y[0]

            if s in s_i_we_care:
                s_i_index = s_i_we_care.index(s)
                e_i = e_i_we_care[s_i_index]

                x = subtract_vectors(y,e_i)

    words_corrected.append(x)
    xs.append(x[:k])

xs = conv_list_2_to_3(xs)
print_xs()

print('------------')

# =====================
# Part 2
# =====================

words_corrected = []
xs = []

for y in words_received_part_2:

    # there are from 2 to 3 '*' symbols in a word
    # replace every '*' with 0,1,2 to get all possible
    # words before deletion happened
    #
    # if there were 2 '*', we get 3^2 = 9 words
    # if 3 '*': 3^3 = 27 words
    words = [[]]

    for i in range(y.count('*')):
        temp = []
        star_index = y.index('*')

        y_before_star = y[:star_index]
        y = y[star_index+1:]

        for w in words:
            for symbol in [[0],[1],[2]]:
                temp.append(w + y_before_star + symbol)

        words = temp[:]

    # add the remaining part
    # of y to every word
    for w in words:
        w += y

    for w in words:
        if mult([w],H_T) == [n_minus_k_zeroes]:
            words_corrected.append([w][0])
            break

for w in words_corrected:
    xs.append(w[:k])

xs = conv_list_2_to_3(xs)
print_xs()
