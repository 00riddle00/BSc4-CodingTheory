
import copy
import math
import random

#################################################
# Helper functions
#################################################

def nCr(n,r):
    return \
        math.factorial(n) / (math.factorial(n-r) * math.factorial(r))

# p(c,d)
def prob_c_and_d(p,c,d):
    c_idx = codes.index(c)
    return p_codes[c_idx] * prob_d_cond_c(p,d,c)

# p(d|c)
def prob_d_cond_c(p,d,c):
    t=1
    for i in range(0,8):
        t*=p[c[i]][d[i]]
    return t

#################################################
# Functions
#################################################

## Calculate Hamming distance
## h(u,v), u,v in F_p_k
def h(u,v):
    d = 0
    k = min(len(u),len(v))
    for i in range(0,k):
        if u[i] != v[i]:
            d += 1
    return d

# Volume of a circle
# V_q(r) = |B_q(r,c)|
def V_q_r(q,r):
    res = 0
    for i in range(r+1):
        res += nCr(n,i) * (q-1)**i
    return res

# Number of errors that are fixed
def errfix_count(d):
    return int((d-1)/2)

# Calculate lower/upper bounds for max code length
def get_Aq_bounds(q,n,d):
    return [(q**n) / V_q_r(q,d-1), (q**n) / V_q_r(q,t)]

## Generate all k-length words from F_p
## F_p = {0,1,2,3,...,p-1}
## Result: F_p_k
def generate_all_codes(n, arr, i):
    if i == n:
        all_codes.append(''.join(str(e) for e in arr))
        return

    arr[i] = 0
    generate_all_codes(n, arr, i + 1)

    arr[i] = 1
    generate_all_codes(n, arr, i + 1)

# Run this function multiple times while searching
# for the longest code
def remove_from_circle():
    for start_idx in range(256):
        ## From the circle C removes elements in radius r, but leaves its center c
        remaining_codes_bf = all_codes[:]
        remaining_codes_af = all_codes[:]
        codes = []
        indices = []

        c1 = remaining_codes_bf.pop(start_idx)
        codes.append(c1)
        remaining_codes_af.pop(start_idx)

        while len(remaining_codes_af):
            for c_i, code in enumerate(remaining_codes_bf):
                _h = h(c1,code)
                if _h in range(1,d):
                    remaining_codes_af.remove(code)

            if len(remaining_codes_af):
                idx = random.randint(0, len(remaining_codes_af)-1)
                c1 = remaining_codes_af.pop(idx)
                indices.append(idx)
                codes.append(c1)
                remaining_codes_bf = remaining_codes_af[:]

        # increment the code_len until no more results appear
        # after multiple runs of this "for loop"
        code_len = 18
        if len(codes) == code_len:
            print('start_idx=', start_idx)
            print('indices=', indices)
            for code_word in codes:
                print(code_word)
            print(len(codes))
            print()

#################################################
# Main
#################################################

# [1] find the largest code M, given the the length n
# and minimum distance d.

# [2] Create the following table:
#     code word c | distance to the nearest code word

# [3] Calculate the probability of "deceiving" when
# using this code, where symmetric channel distortion
# probability is given

q = 2
n = 8
d = 3
t = errfix_count(d)

p = [[0.95,0.05],
     [0.05,0.95]]

print('A_2(8,3) bounds:', get_Aq_bounds(q,n,d))
print()

all_codes = []
arr = [None] * n

generate_all_codes(n, arr, 0)

#remove_from_circle()
#remove_from_circle()
#remove_from_circle()
#remove_from_circle()
#remove_from_circle()

# chosen indices and codes (by running the remove_from_circle() function multiple times)
start_idx= 205
indices= [103, 30, 91, 64, 31, 13, 54, 51, 35, 7, 5, 8, 3, 6, 4, 0, 0, 0]
chosen_codes = ['11001101',
                '01101111',
                '00100000',
                '10100101',
                '10000011',
                '01000110',
                '00011101',
                '11011011',
                '11110111',
                '11000000',
                '00111110',
                '01110001',
                '10110010',
                '10010100',
                '11111100',
                '11101010',
                '00001010',
                '01011000',
                '10111001']


# Calculate minimum distance to the nearest code word (for all code words)
min_dists = []
for c in chosen_codes:
    min_dist = 8
    for c_closest in chosen_codes:
        dist = h(c,c_closest)
        if dist > 0:
            if dist < min_dist:
                min_dist = dist
    min_dists.append(min_dist)

# Results table together with the probability of "deceiving"
print('Sent code word | Distance to the nearest code word | Probability of "deceiving"')
for ii in range(len(chosen_codes)):
    chosen_codes_tmp = chosen_codes[:]
    c1 = chosen_codes_tmp.pop(ii)
    prob_c1_to_c_i = 0
    for c_i in chosen_codes_tmp:
        prob_c1_to_c_i += prob_d_cond_c(p,[int(i) for i in list(c_i)],[int(i) for i in list(c1)])
    print(f'c{ii+1:02} ({chosen_codes[ii]}) | {min_dists[ii]} | {prob_c1_to_c_i}')
