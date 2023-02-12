import math

# Assume 3 copies of Lora data
# Spreading Factor
SF = 8
# num_data_word_symbol
M = 20 - 2
# num_fcs_symbol
m = 2 + 2
# decode symbols
t = 5
# prob_symbol_transmit_correct
p0 = 0.95
# num_bits 
N = 2 ** SF
# decode probability
DECODE_PASS = p0**t
DECODE_FAIL = 1 - DECODE_PASS


def prob_distinct(n, k):
	return math.factorial(n) / (n**k * math.factorial(n - k))

def prob_com(n, k, p):
	return math.comb(n, k) * (p**k) * ((1-p)**(n-k) )

def check_all(c):
	return prob_CRC_pass(c) + fail_all_major_correct(c) + fail_one_symbol_lookup(c , 1) + fail_one_symbol_lookup(c , 2) + unrecover(c)

def prob_CRC_pass_no_decode(c):
	return (1 - ((1 - p0**(M + m))**c))

def prob_CRC_pass(c):
	res = 0
	if c == 0:
		return res
	else:
		for i in range(1, c+1):
			res += prob_CRC_pass_no_decode(i) * prob_com(c, i, DECODE_PASS)
	return res;

def prob_no_CRC_pass(c):
	return 1 - prob_CRC_pass(c)

def at_least_one_correct_CRC_no_decode(c):
	return 1 - ((1 - p0**(m))**c)

def major_correct_symbol(c):
	res = 0
	if c == 0 or c == 1:
		return res
	else:
		for i in range(2, c+1):
			res += prob_com(c, i, p0) * prob_distinct(N - 1, c - i)
	return res

def fail_all_major_correct(c):
	res = 0
	if c == 0 or c == 1 or c == 2:
		return 0
	else:
		for i in range (3, c+1):
			temp = prob_com(M, M, major_correct_symbol(i)) * at_least_one_correct_CRC_no_decode(i) - prob_CRC_pass_no_decode(i)
			# print(temp)
			res += temp * prob_com(c, i, DECODE_PASS)
	return res

def fail_j_symbol_lookup(c, j):
	res = 0
	if c == 0 or c == 1:
		return 0
	elif c == 2:
		res = prob_com(M, M-j, major_correct_symbol(2))* at_least_one_correct_CRC_no_decode(2) * (1 - prob_CRC_pass_no_decode(2)) / (1 - prob_com(M, M, major_correct_symbol(2))) * prob_com(2, 2, DECODE_PASS)
		# print(res)
	else:
		# print(res)
		res += fail_j_symbol_lookup(2, j) / prob_com(2, 2, DECODE_PASS) * prob_com(c, 2, DECODE_PASS)
		# print(res)
		for i in range (3, c+1):
			temp = prob_com(M, M-j, major_correct_symbol(i))* at_least_one_correct_CRC_no_decode(i)
			res += temp * prob_com(c, i, DECODE_PASS)
			# print(res)
	return res

def fail_j_symbol_lookup_no_decode(c, j):
	return prob_com(M, M-j, major_correct_symbol(c))* at_least_one_correct_CRC_no_decode(c)

def unrecover(c):
	res = 0
	if c == 0:
		return 1
	elif c == 1:
		return 1 - prob_CRC_pass(1)
	else:
		res += 1 * prob_com(c, 0, DECODE_PASS) + (1 - prob_CRC_pass_no_decode(1)) * prob_com(c, 1, DECODE_PASS)
		for i in range (2, c+1):
			temp = 1 - at_least_one_correct_CRC_no_decode(i)
			res += temp * prob_com(c, i, DECODE_PASS)
	# return  1 - prob_CRC_pass(c) - fail_all_major_correct(c) - fail_one_symbol_lookup(c, 1) - fail_one_symbol_lookup(c, 2)
	return res

c = 3
# print(major_correct_symbol(c))
# print(no_major_symbol(c))
# print(1-major_correct_symbol())
# print(1 - at_least_one_correct_CRC_no_decode(c))
print(prob_CRC_pass(c))
# print(prob_CRC_pass_no_decode(2))
print(fail_all_major_correct(c))
for j in range(1, 5):
	print(fail_j_symbol_lookup(c, j))
# print(fail_two_symbol_lookup())
print(unrecover(c))
# print(fail_j_symbol_lookup_no_decode(2, 4))
# print(check_all(c))
# print(prob_com(c, 0, DECODE_PASS))
# print(prob_com(c, 1, DECODE_PASS))
# print(prob_com(c, 2, DECODE_PASS))
# print(prob_com(c, 3, DECODE_PASS))
# print(prob_CRC_pass_no_decode(c))
# print(fail_j_symbol_lookup_no_decode(c, 0))
# print(fail_j_symbol_lookup_no_decode(c, 1))
# print(fail_j_symbol_lookup_no_decode(c, 2))
# print(fail_j_symbol_lookup_no_decode(c, 3))
# print(fail_j_symbol_lookup_no_decode(c, 4))
# print(fail_j_symbol_lookup_no_decode(c, 5))
