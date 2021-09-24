
# ==========================================================
# Helper functions
# ==========================================================

# =============================
# Entropy
# =============================

# H(X)
# P - the list of probabilities
def H(P):
    e = 0
    for t in P:
        e += t*log(1/t,2)
    return(N(e))

# H(X|Y=d)
def H_X_cond_Y(p,d):
    return H([prob_c_cond_d(p,c1,d),
              prob_c_cond_d(p,c2,d),
              prob_c_cond_d(p,c3,d)])

# =============================
# Probabilities
# =============================

# p(c,d)
def prob_c_and_d(p,c,d):
    c_idx = codes.index(c)
    return p_codes[c_idx] * prob_d_cond_c(p,d,c)

# p(d|c)
#
# distortion probability, where
#     c=[x1,x2,x3] -> [y1,y2,y3]=d
# If c == d, the return value means the probability
# of correctly transmitting bits
def prob_d_cond_c(p,d,c):
    t=1
    for i in range(0,3):
        t*=p[c[i]][d[i]]
    return t

# p(c|d)
def prob_c_cond_d(p,c,d):
    return prob_c_and_d(p,c,d) / prob_received_d(p,d)

# p(d)
def prob_received_d(p,d):
    return p_c1*prob_d_cond_c(p,d,c1) + \
           p_c2*prob_d_cond_c(p,d,c2) + \
           p_c3*prob_d_cond_c(p,d,c3)

# ==========================================================
# Main functions
# ==========================================================

def calc_correct_transfer_prob(decod_groups):
    prob = 0
    for i,group in enumerate(decod_groups):
        _sum = 0
        for d in group:
            _sum += prob_d_cond_c(p,d,codes[i])
        prob += p_codes[i]*_sum
    return prob

def calc_decoding_groups(decod_rule):
    decod_groups = \
        [c1_group, c2_group, c3_group] = [[],[],[]]

    for d in recv:
        _max = 0
        for i,c in enumerate(codes):
            if decod_rule == 'MLD':
                p_d_c = prob_d_cond_c(p,d,c)
            elif decod_rule == 'IOD':
                p_d_c = p_codes[i]*prob_d_cond_c(p,d,c)
            if p_d_c > _max:
                _max = p_d_c
                max_idx = i

        decod_groups[max_idx].append(d)
    return decod_groups

def print_decoding_groups(decod_groups):
    for i,group in enumerate(decod_groups):
        group_str_lists = [''.join([str(j) for j in d]) for d in group]
        group_str = ', '.join(group_str_lists)
        c_i_str = ''.join([str(j) for j in codes[i]])
        print(f'c{i+1} ({c_i_str}) is decoded from: {group_str}')

# ==========================================================
# Main
# ==========================================================

# Channel's probabilities
# p = [[p_00,p_01],
#      [p_10,p_11]]
p = [[0.82,0.18],
     [0.25,0.75]]

# Code words
codes = [c1,c2,c3] = [[0,1,0],
                      [1,0,0],
                      [0,1,1]]

# Source's probabilities
p_codes = [p_c1,p_c2,p_c3] = [0.24, 0.23, 0.53]

# All the words that can possibly be received
recv = [d1,d2,d3,d4,d5,d6,d7,d8] = [[0,0,0],
                                    [0,0,1],
                                    [0,1,0],
                                    [0,1,1],
                                    [1,0,0],
                                    [1,0,1],
                                    [1,1,0],
                                    [1,1,1]]

# [1] Correct transfer probability (without (de)coding)
p1 = p_c1*prob_d_cond_c(p,c1,c1) + \
     p_c2*prob_d_cond_c(p,c2,c2) + \
     p_c3*prob_d_cond_c(p,c3,c3)

print(f'p1 = {p1}\n')

# [2] Create MLD (Maximum likelihood decoding) rule
decod_groups = calc_decoding_groups('MLD')
print("MLD rule:")
print_decoding_groups(decod_groups)

# [2.1] Correct transfer probability (using MLD)
p2 = calc_correct_transfer_prob(decod_groups)
print(f'p2 = {p2}\n')

# [3] Create IOD (Ideal observer decoding) rule
decod_groups = calc_decoding_groups('IOD')
print("IOD rule:")
print_decoding_groups(decod_groups)

# [3.1] Correct transfer probability (using IOD)
p3 = calc_correct_transfer_prob(decod_groups)
print(f'p3 = {p3}\n')

# [4] Information amount transfered in a channel (without (de)coding)
_H = H(p_codes)

H_X_Y = 0
for d in recv:
    H_X_Y += prob_received_d(p,d)*H_X_cond_Y(p,d)

I_X_Y = _H - H_X_Y
print(f'I(X,Y) without coding: {I_X_Y}')

# [4] Information amount transfered in a channel (using MLD or IOD)
H_X_Y = 0

# here d is one of c1,c2,c3 since decoding is performed
for d in [c1,c2,c3]:
    H_X_Y += prob_received_d(p,d)*H_X_cond_Y(p,d)

I_X_Y = _H - H_X_Y
print(f'I(X,Y) with MLD or IOD: {I_X_Y}')
