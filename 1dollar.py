#!/usr/bin/env python3

import random

N = 100
Cycles = 100

random.seed()
# warmup
for i in range(10000):
	random.randrange(N)

for i in range(1, 1000):
	p = [N] * N
	for j in range(i * Cycles):
		for k in range(N):
			if p[k] > 0:
				while True: # make sure to give away money to another person
					to = random.randrange(N)
					if to != k:	break
				p[k] -= 1
				p[to] += 1
	q = sorted(p)
	pmin = q[0]
	pmax = q[-1]
	md = q[N // 2]
	q1 = sum(q[:N // 4]) * 4.0 / N
	q3 = sum(q[-N // 4:]) * 4.0 / N
	print('n = {:6} => min/max/Δ/Md/Q1/Q3: '
		'{:5d} {:5d} {:5d} {:5d} {:6.1f} {:6.1f}'
		.format(i * Cycles, pmin, pmax, pmax - pmin, md, q1, q3))
