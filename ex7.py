
c1 = [10, 8, 19, 11, 15, 0, 28, 6, 27, 29, 12, 7, 14, 2, 2, 14, 7, 12, 29, 27, 6, 28, 0, 15, 11, 19, 8, 9, 22, 16, 22]
c2 = [14, 21, 17, 1, 4, 26, 5, 3, 20, 25, 18, 30, 30, 18, 25, 20, 3, 5, 26, 4, 1, 17, 21, 13, 24, 23, 10, 16, 10, 23, 24]
c3 = [15, 14, 28, 28, 8, 5, 17, 13, 24, 19, 29, 23, 1, 25, 2, 25, 1, 23, 29, 19, 24, 13, 17, 5, 8, 26, 28, 14, 15, 0, 0]

c = c1 # visi vienetai - 1-as stulpelis
#c = c2 # visi vienetai - 1-as stulpelis
#c = c3 # 4-as stulpelis * 2 atrodo, bet neaktualu mums.

alph = "AĄBCČDEĘĖFGHIĮYJKLMNOPRSŠTUŲŪVZ"
q=31
f0=[1 for i in range(0,31)]
f1 = [i^1%q for i in range(1,32)]
f2 = [i^2%q for i in range(1,32)]

K = [f0,f1,f2]

for i in range(3,28):
    K.append([j^i%q for j in range(1,32)])

print("Kontroline matrica:")
for line in K:
    print(line)
print()


syndrome = [0 for x in range(0,28)]

for i in range(0,28):
    sum = 0
    for j in range(0,31):
        sum = (sum + K[i][j]*c[j] ) % q
    syndrome[i] = sum

print(syndrome)
print()

# pataisyta:
c1 = [9, 8, 19, 11, 15, 0, 28, 6, 27, 29, 12, 7, 14, 2, 2, 14, 7, 12, 29, 27, 6, 28, 0, 15, 11, 19, 8, 9, 22, 16, 22]
c2 = [13, 21, 17, 1, 4, 26, 5, 3, 20, 25, 18, 30, 30, 18, 25, 20, 3, 5, 26, 4, 1, 17, 21, 13, 24, 23, 10, 16, 10, 23, 24]
c3 = [15, 14, 28, 28, 8, 5, 17, 13, 24, 19, 29, 23, 1, 25, 2, 25, 1, 23, 29, 19, 24, 13, 17, 5, 8, 26, 28, 14, 15, 0, 0]

# x1+x2+x3=9
# x1+2*x2+4*x3=8
# x1+3*x2+9*x3=19
#
# ATS: x = 22 and y = -19 and z = 6

# ...=13
# ...=21
# ...=17
#
# ATS: x = -7 and y = 26 and z = -6

# ...=15
# ...=14
# ...=28
#
# ATS: x = 31 and y = -47/2 and z = 15/2

print((22)%31)
print((-19)%31)
print((6)%31)
print()
print((-7)%31)
print((26)%31)
print((-6)%31)
print()
print((31)%31)
print((-47/2)%31)
print((15/2)%31)
print()

22
12
6

24
26
25

0
23
23

letters = [22,12,6,
           24,26,25,
           0,23,23]

for i in range(0,9):
    print(alph[letters[i]])
