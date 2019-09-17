""" PARSES AND SOLVES A QUADRATIC EQUATION """

eq = input('Enter an equation: ')

a = eq.split('x^2')[0]
if len(a) == 0:
    a = 1

t = []
temp = eq.split('+')
for c, i in enumerate(temp):
    temp[c] = i.split('-')

for i in temp:
    if type(i) == list:
        for j in i:
            t.append(j)
    else:
        t.append(i)

sign = eq.split(t[0])[-1].split(t[-1])[0].split(t[1])
if sign[0] == '+':
    b = t[1].split('x')[0]
else:
    b = (sign[0]+ t[1]).split('x')[0]

if sign[1] == '+':
    c = t[2]
else:
    c = sign[1] + t[2]
print(t)
print(a, b, c)

import math

# calc_quadratic computes the result of a quadratic equation
def calc_quadratic(a, b, c):
    disc = (b**2.0) - 4.0*a*c
    two_a = 2.0 * a
    minus_b = -1.0 * b

    if disc < 0:
        disc = disc * -1.0
        sq_disc = math.sqrt(disc)
        res = "%f +/- %fi" % ((minus_b/two_a), (sq_disc/two_a))
    else:
        sq_disc = math.sqrt(disc)
        x1 = (minus_b/two_a) + (sq_disc/two_a)
        x2 = (minus_b/two_a) - (sq_disc/two_a)
        res = "%f, %f" % (x1, x2)

    return res

res = calc_quadratic(int(a), int(b), int(c))
print(res)
