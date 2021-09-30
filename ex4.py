
# ====================================
# Helper functions
# ====================================

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def negative(M):
    return [[(-1 * M[i][j]) % q  for j in range(len(M))] for i in range(len(M[0]))]

def concat(M,N):
    return [M[i] + N[i] for i in range(len(M))]

def mult(M,N):
    result = [[0 for j in range(len(N[0]))] for i in range(len(M))]

    for i in range(len(M)):
        for j in range(len(N[0])):
            for k in range(len(N)):
                result[i][j] = (result[i][j] + M[i][k] * N[k][j]) % q

    return result

def subtract_vectors(u,v):
    return [(u[i] - v[i]) % q for i in range(len(u))]

# ====================================
# Main
# ====================================

text_abc = ['A', 'B', 'C', 'Č', 'D', 'E', 'Ė', 'F', 'G',
            'H', 'I', 'Y', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'R', 'S', 'Š', 'T', 'U', 'V', 'Z', 'Ž']

n = 6
q = 3
q_zeroes = [[0 for i in range(q)]]

words_received = \
    [[2, 0, 2, 2, 1, 0],
     [1, 1, 2, 1, 1, 2],
     [1, 0, 1, 0, 2, 2],
     [0, 0, 2, 1, 0, 2],
     [2, 0, 2, 2, 2, 0],
     [2, 2, 2, 1, 0, 1],
     [2, 0, 2, 0, 1, 1],
     [2, 2, 2, 0, 1, 2],
     [2, 1, 0, 2, 0, 0],
     [1, 1, 1, 0, 2, 1],
     [0, 0, 0, 2, 0, 0],
     [0, 0, 2, 2, 1, 1]]

G = [[1, 0, 0, 0, 2, 1],
     [0, 1, 0, 2, 2, 0],
     [0, 0, 1, 1, 0, 1]]

I = [[1, 0, 0],
     [0, 1, 0],
     [0, 0, 1]]

A = [[G[0][3], G[0][4], G[0][5]],
     [G[1][3], G[1][4], G[1][5]],
     [G[2][3], G[2][4], G[2][5]]]

A_T = transpose(A)

minus_A_T = negative(A_T)

H = concat(minus_A_T, I)

H_T = transpose(H)


all_zeroes = [0] * n
e_i_all = []

for i in range(n):
    e_i_first = all_zeroes[:]
    e_i_second = all_zeroes[:]

    e_i_first[i] = 1
    e_i_second[i] = 2

    e_i_all.append(e_i_first)
    e_i_all.append(e_i_second)


s_i_all = mult(e_i_all,H_T)

words_corrected = []
xs = []

for y in words_received:
    y = [y]
    s = mult(y,H_T)

    if s != q_zeroes:
        s = s[0]
        y = y[0]

        s_i_index = s_i_all.index(s)
        e_i = e_i_all[s_i_index]

        x = subtract_vectors(y,e_i)
        words_corrected.append(x)
        xs.append(x[:q])

print('Gautas žodis|Ištaisytas žodis')
for i in range(len(words_received)):
    received_word = ''.join(str(x) for x in (words_received[i]))
    correct_word = ''.join(str(x) for x in (words_corrected[i]))

    if received_word == correct_word:
        correct_word = '(Klaidų nebuvo)'

    print(f'{received_word}      | {correct_word}')

print()
for x in xs:
    letter_index = x[0] + x[1] * 3 + x[2] * 9
    print(text_abc[letter_index], end='')
