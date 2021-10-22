
# ====================================
# Helper functions
# ====================================

## Generate all K-length words from F_p
## F_p = {0,1,2,3,...,p-1}
## Result: F_p_k
def generate_all_words(K, p, arr, i):
    if i == K:
        all_codes.append(''.join(str(e) for e in arr))
        return

    for j in range(p):
        arr[i] = j
        generate_all_words(K, p, arr, i + 1)

# Matrix multiplication
def mult(M,N):
    result = [[0 for j in range(len(N[0]))] for i in range(len(M))]

    for i in range(len(M)):
        for j in range(len(N[0])):
            for l in range(len(N)):
                result[i][j] = (result[i][j] + M[i][l] * N[l][j]) % q

    return result

# ====================================
# Main functions
# ====================================

# get code's weights distribution A
def get_A(code):
    A=[0] * (n+1) # = [A_0,A_1,...,A_n]
    for c in code:
        i=0
        for e in c:
            if e>0:
                i+=1
        A[i]+=1
    return A

def w_L_in_McWilliams_RHS(A):
    var('y')
    w_L_RHS = 0
    for i in range(n+1):
        w_L_RHS += A[i]*((q-1)*y+1)^(n-i)*(1-y)^i
    return w_L_RHS

# Probability of deception for any code word
# (calculated for zeroeth word '00...0', but
# applies to any other code word as well)
#
# p - distortion probability
def p_deception(A, p):
    A_dict = {
        weight: word_count for weight, word_count in enumerate(A)}
    P = 0
    for i in range(1,n+1):
        P += A_dict[i]*p^i*(1-p)^(n-i)
    return P

# ====================================
# Main
# ====================================

q=5 # alphabet size
n=6 # length of code word

# =====================
# Part 1
# =====================

# We need to weigh the code L, given it's control
# matrix (=gen. matrix of its dual code)

# We also need to find the probability of deception,
# in cases where p = 0.1 and p = 0.05

# Control matrix of the code L
H=[[1,3,1,0,0,1],
   [1,0,4,2,1,0]]

k_dual = len(H)
k = n - k_dual

L_dual_size = q^k_dual
L_size = q^k

# Composing L's dual code
L_dual = []

# generate all symbol sequences of
# length k_dual from alphabet q
all_codes = []
arr = [None] * k_dual
generate_all_words(k_dual, q, arr, 0)

all_seqs = all_codes # just for naming
all_seqs_as_matrices = [[[int(x) for x in list(seq)]] for seq in all_seqs]

for seq in all_seqs_as_matrices:
    word = mult(seq, H)[0]
    L_dual.append(word)

assert len(L_dual) == L_dual_size

# L_dual's weight distribution
A_L_dual = get_A(L_dual)
assert sum(A_L_dual) == L_dual_size

# Composing weight distribution function
# (needed to find w_L: weight distribution of code L)
w_L_dual = w_L_in_McWilliams_RHS(A_L_dual)
w_L = expand(w_L_dual)/L_dual_size

A_L = w_L.list()
while len(A_L) < (n+1):
    A_L.append(0)

assert sum(A_L) == L_size

print('weight | number of code words')
for weight, num_of_words in enumerate(A_L):
    print(f'{weight}      | {num_of_words}')
print()

print(f'p =  0.1, P(deception) = {p_deception(A_L, 0.1)}')
print(f'p = 0.05, P(deception) = {p_deception(A_L, 0.05)}')
print()

# =====================
# Part 2
# =====================

q=5 # alphabet size
n=6 # length of code word

# We need to weigh a self-dual code

# Generating matrix of the self-dual code
#
# We won't be needing this matrix at all
# The only important thing is the knowledge
# that such code exists (n=6, q=5)
#
G = H = [[1,1,1,1,1,0],
         [1,2,3,4,0,0],
         [1,4,4,1,0,1]]

k_self_dual = len(H)
L_self_dual_size = q^k_self_dual

# Elements of code's weight distribution
var('y,a0,a1,a2,a3,a4,a5,a6')
A = [a0,a1,a2,a3,a4,a5,a6]

# Composing weight distribution function
# (needed to find coefficients of w_L_self_dual)
w_L_self_dual_in_LHS = 0

for i in range(n+1):
    w_L_self_dual_in_LHS += A[i]*y^i
# w_L_self_dual_in_LHS =
#     a6*y^6 + a5*y^5 + a4*y^4 + a3*y^3 + a2*y^2 + a1*y + a0

w_L_self_dual_in_RHS = 0
for i in range(n+1):
    w_L_self_dual_in_RHS += A[i]*((q-1)*y+1)^(n-i)*(1-y)^i
# w_L_self_dual_in_RHS =
#       a0*(4*y + 1)^6
#     - a1*(4*y + 1)^5*(y - 1)
#     + a2*(4*y + 1)^4*(y - 1)^2
#     - a3*(4*y + 1)^3*(y - 1)^3
#     + a4*(4*y + 1)^2*(y - 1)^4
#     - a5*(4*y + 1)*(y - 1)^5
#     + a6*(y - 1)^6

# expr should be 0
expr = w_L_self_dual_in_LHS - w_L_self_dual_in_RHS/L_self_dual_size

# Finding coefficients a0,a1,...,a6
# We know (from theory) that a0 = 1, a1 = 0, a2 = 0, a3 = 0
c = expr.coefficients(y)

solution = solve([
    c[0][0]==0,
    c[1][0]==0,
    c[2][0]==0,
    c[3][0]==0,
    c[4][0]==0,
    c[5][0]==0,
    c[6][0]==0,
    a0==1,
    a1==0,
    a2==0,
    a3==0],
    a0,a1,a2,a3,a4,a5,a6)

solution = solution[0]

A_L_self_dual = [solution[i].rhs() for i in range(len(solution))]

print('weight | number of code words')
for weight, num_of_words in enumerate(A_L_self_dual):
    print(f'{weight}      | {num_of_words}')
print()
