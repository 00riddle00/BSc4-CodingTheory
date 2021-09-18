
# ==========================================================
# Functions
# ==========================================================

def calc_decoding_groups(decod_rule):
    decod_groups = [c1_group, c2_group, c3_group] = [[],[],[]]
    for d in recv:
        imax = 0
        for i,c in enumerate(codes):
            if decod_rule == 'DTT':
                p_d_c = tikimybe(p,d,c)
            elif decod_rule == 'IST':
                p_d_c = p_codes[i]*tikimybe(p,d,c)
            if p_d_c > imax:
                imax = p_d_c
                imax_idx = i

        decod_groups[imax_idx].append(d)
    return decod_groups

def print_decoding_groups(decod_groups):
    for i,group in enumerate(decod_groups):
        group_str_lists = [''.join([str(j) for j in d]) for d in group]
        group_str = ', '.join(group_str_lists)
        c_i_str = ''.join([str(j) for j in codes[i]])
        print(f'c{i+1} ({c_i_str}) is decoded from: {group_str}')

def calc_rule_prob(decod_groups):
    prob = 0
    for i,group in enumerate(decod_groups):
        _sum = 0
        for code in group:
            _sum += tikimybe(p,codes[i],code)
        prob += p_codes[i]*_sum
    return prob

# Iškraipymo x= [x_1,x_2,x_3]->[y_1,y_2,y_3]=y tikimybės skaičiavimas
# Jei x == y, apskaičiuojama teisinga bitų perdavimo tikimybė
# Kanalo tikimybės p=[[p_00,p_01],[p_10,p_11]]
def tikimybe(p,x,y):
    t=1
    for i in range(0,3):
        t*=p[x[i]][y[i]]
    return t

# ==========================================================
# Main
# ==========================================================

# Kanalo tikimybės
p=[[0.82,0.18],
   [0.25,0.75]]

# Kodo žodžiai
codes = [c1,c2,c3] = [[0,1,0],
                      [1,0,0],
                      [0,1,1]]

# Šaltinio tikimybės
p_codes = [p_c1,p_c2,p_c3] = [0.24, 0.23, 0.53]

# Visi žodžiai, kuriuos įmanoma gauti
recv = [d1,d2,d3,d4,d5,d6,d7,d8] = [[0,0,0],
                                    [0,0,1],
                                    [0,1,0],
                                    [0,1,1],
                                    [1,0,0],
                                    [1,0,1],
                                    [1,1,0],
                                    [1,1,1]]

# [0] Teisingo perdavimo tikimybės vidurkis be kodavimo
p0 = p_c1*tikimybe(p,c1,c1) + p_c2*tikimybe(p,c2,c2) + p_c3*tikimybe(p,c3,c3)
print(f'p0 = {p0}\n')

# [1] DTT taisyklės sudarymas
decod_groups = calc_decoding_groups('DTT')
print_decoding_groups(decod_groups)

# [1.1] Teisingo perdavimo tikimybės vidurkis su DTT
p1 = calc_rule_prob(decod_groups)
print(f'p1 = {p1}\n')

# [2] IST taisyklės sudarymas
decod_groups = calc_decoding_groups('IST')
print_decoding_groups(decod_groups)

# [2.1] Teisingo perdavimo tikimybės vidurkis su IST
p2 = calc_rule_prob(decod_groups)
print(f'p2 = {p2}\n')
