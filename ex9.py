# Užduotyje duoti trys Hammingo kodo H5(2) žodžiai, gauti iš kanalo.
# Kiekviename žodyje arba vienas simbolis iškraipytas, arba vienas ar du ištrinti.
# Ištaisykite įvykusias klaidas ir atkurkite siųstą informaciją (12 raidžių žodį).

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

def mult_without_modulo(M,N):
    result = [[0 for j in range(len(N[0]))] for i in range(len(M))]

    for i in range(len(M)):
        for j in range(len(N[0])):
            for l in range(len(N)):
                result[i][j] = (result[i][j] + M[i][l] * N[l][j])

    return result

# convert zs - lists of 4 elems -> to lists of 2 elems
# TODO fix this function and apply fixes in other files
def conv_list_4_to_2(zs):
    flat_zs = [item for sublist in zs for item in sublist]
    return [flat_zs[i:i + 2] for i in range(0, len(flat_zs), 2)]

# 16 užduotis
# Žodis, parašytas abėcėlės
text_abc = ['A', 'B', 'C', 'D', 'E',
            'Ė', 'F', 'G', 'H', 'I',
            'Y', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'R', 'S',
            'Š', 'T', 'U', 'V', 'Z']

# raidėmis buvo koduotas Hamingo H_5(2)  kodu.

n = 6
q = 5
k = 4
n_minus_k_zeroes = [0] * (n-k)

# Naudota generuojanti matrica

G = [[1, 0, 0, 0, 4, 1],
     [0, 1, 0, 0, 3, 4],
     [0, 0, 1, 0, 4, 3],
     [0, 0, 0, 1, 4, 4]]

# Kanale arba vienas simbolis išsikraipė, arba vienas ar du išsitrynė.
# Gauti iš kanalo žodžiai:

words_received = \
d0 = [2, 2, 0, 1, 0, 1]
d1 = [1, 4, '*', '*', 4, 2]
d2 = [4, 0, 4, 2, 3, 3]
d3 = [2, 3, 0, 0, 0, 3]
d4 = [3, 4, '*', 4, '*', 4]
d5 = [0, 2, 0, 4, 3, 0]

# Ištaisykite iškraipymus ir atkurkite siųstą žodį

A = [[G[0][4], G[0][5]],
     [G[1][4], G[1][5]],
     [G[2][4], G[2][5]],
     [G[3][4], G[3][5]]]

I_2 = [[1, 0],
       [0, 1]]

A_T = transpose(A)

minus_A_T = negative(A_T)

H = concat(minus_A_T, I_2)

H_T = transpose(H)

#================
# Case 1
#================
syndromes = mult([d0,d2,d3,d5],H_T)

for row in H:
    print(row)
print()

print(syndromes)

d0[3] = (d0[3] - 2) % q
d2[1] = (d2[1] - 4) % q
d3[1] = (d3[1] - 4) % q
d5[3] = (d5[3] - 2) % q

#================
# Case 2
#================

var('x','y')
d1 = [1, 4, x, y, 4, 2]
# NOTE: here matrix multiplication is
# performed without modulo q
eq = mult_without_modulo([d1],H_T)[0]

solution = solve([eq[0]==0,eq[1]==0],x,y)

x = int(solution[0][0].rhs()) % q
y = int(solution[0][1].rhs()) % q

d1 = [1, 4, x, y, 4, 2]

#-----------------

var('x','y')
d4 = [3, 4, x, 4, y, 4]
eq = mult_without_modulo([d4],H_T)[0]

solution = solve([eq[0]==0,eq[1]==0],x,y)

x = int(solution[0][0].rhs()) % q
y = int(solution[0][1].rhs()) % q

d4 = [3, 4, x, 4, y, 4]

#================
# Results
#================

xs = [d0[:4],
      d1[:4],
      d2[:4],
      d3[:4],
      d4[:4],
      d5[:4]]

xs = conv_list_4_to_2(xs)

print()
for x in xs:
    letter_index = x[0] * 5 + x[1]
    print(text_abc[letter_index], end='')
