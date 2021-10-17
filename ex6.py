

def McWilliams_RHS_w_L(A):
    var('y')
    suma = 0
    for i in range(n+1):
        suma += A[i]*((q-1)*y+1)^(n-i)*(1-y)^i
    return suma

# Užduotis - surasti duoto kodo ir jam dualaus kodo svorius
# bei ,,apgavystės" tikimybes. Pasinaudokite MacWilliams tapatybe.

# 8 užduotis

# Abėcėlės dydis q=5
# Kontrolinės kodo matricos eilutės:
# 131001, 104210.
# Raskite kodo svorius ir ,,apgavystės tikimybę``, kai p=0,1 ir p=0,05.

# Savidualaus kodo L generuojančios matricos eilutės:
# 111110, 123400, 144101
# Raskite L svorių skirstinį.

q=5
n=6

# ------------------------------ part 1 ---------------------------

# H yra kodo L_dualus generuojanti matrica
H=[[1,3,1,0,0,1],
   [1,0,4,2,1,0]]

k_dualus = len(H)
k = n - k_dualus

L_dualus_size = q^k_dualus
L_size = q^k

# Kodo L_dualus sudarymas
L_dualus = []

for i in range(0,q):
    for j in range(0,q):
        c=[]
        for l in range(0,n):
            c.append((i*H[0][l]+j*H[1][l])%q)
        L_dualus.append(c)

assert len(L_dualus) == L_dualus_size
print(L_dualus)

# Kodo svėrimas
def get_A(LL):
    w=[0] * (n+1) # = [A_0,A_1,...,A_n]
    for c in LL:
        i=0
        for e in c:
            if e>0:
                i+=1
        w[i]+=1
    return w

# Dualaus kodo svorių skirstinys
A_L_dualus = get_A(L_dualus)
assert sum(A_L_dualus) == L_dualus_size
print(A_L_dualus)

# Svorio funkcijos sudarymas
w_L_dualus = McWilliams_RHS_w_L(A_L_dualus)
print(w_L_dualus)

w_L = expand(w_L_dualus)/L_dualus_size
print(w_L)

A_L = w_L.list()
assert sum(A_L) == L_size
print(A_L)

A_L_dict = {weight: num_of_words for weight, num_of_words in enumerate(A_L)}
print(A_L)

#p = 0.1
#p = 0.05

# Probability of deception if 000000 (word of weight 0) was sent
#P = weights_L_dict[1]*p^1*(1-p)^(n-1) + \
#    weights_L_dict[2]*p^2*(1-p)^(n-2) + \
#    weights_L_dict[3]*p^3*(1-p)^(n-3) + \
#    weights_L_dict[4]*p^4*(1-p)^(n-4) + \
#    weights_L_dict[5]*p^5*(1-p)^(n-5) + \
#    weights_L_dict[6]*p^6*(1-p)^(n-6)

#print(P)

print('svoris | kiek tokio svorio žodžių kode')
for weight, num_of_words in enumerate(A_L):
    print(f'{weight}      | {num_of_words}')

# ------------------------------ part 2 ---------------------------

#G = H = [[1,1,1,1,1,0],
#         [1,2,3,4,0,0],
#         [1,4,4,1,0,1]]

# Savidualaus kodo svėrimas
#
# n=6, q=5 kodo svėrimas su MacWilliams tapatybe

# Svorių skirstinio elementai
var('y,a0,a1,a2,a3,a4,a5,a6')

# a0, or 1, same
A = [a0,a1,a2,a3,a4,a5,a6]

# savidualaus kodo svoriu f-ja
#w = 0
#for i in range(n+1):
#    w += A[i]*y^i
#print(w)
# w = a6*y^6 + a5*y^5 + a4*y^4 + a3*y^3 + a2*y^2 + a1*y + a0

w = a6*y^6 + a5*y^5 + a4*y^4 + a0

#ww = 0
#for i in range(n+1):
#    ww += A[i]*((q-1)*y+1)^(n-i)*(1-y)^i
#print(ww)
# ww = a0*(4*y + 1)^6 - a1*(4*y + 1)^5*(y - 1) + a2*(4*y + 1)^4*(y - 1)^2 - a3*(4*y + 1)^3*(y - 1)^3 + a4*(4*y + 1)^2*(y - 1)^4 - a5*(4*y + 1)*(y - 1)^5 + a6*(y - 1)^6

ww = (4*y + 1)^6 + a4*(4*y + 1)^2*(y - 1)^4 - a5*(4*y + 1)*(y - 1)^5 + a6*(y - 1)^6

www=w-ww/125 # turi buti = 0

# isskleisti f-ja, surasti koefus prie y
c=www.coefficients(y)
print(solve([c[0][0]==0,c[1][0]==0,c[2][0]==0,c[3][0]==0,c[4][0]==0,c[5][0]==0,c[6][0]==0],a0,a1,a2,a3,a4,a5,a6))
c
