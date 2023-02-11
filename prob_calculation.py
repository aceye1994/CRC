# Assume 3 copies of Lora data
# Spreading Factor
SF = 8
# num_data_word_symbol
M = 20 - 2
# num_fcs_symbol
m = 2 + 2 + 5
# prob_symbol_transmit_correct
p0 = 0.95
# 
N = 2 ** SF

def check_all():
	return prob_CRC_pass() + fail_all_major_correct() + fail_one_symbol_lookup() + fail_two_symbol_lookup() <= 1

def prob_CRC_pass():
	return 1 - ((1 - p0**(M + m))**3)

def prob_no_CRC_pass():
	return ((1 - p0**(M + m))**3)

def at_least_one_correct_CRC():
	return 1 - (1 - p0	**m)**3

def major_correct_symbol():
	return 3 * p0**2 *(1-p0) + p0**3

def no_major_symbol():
	return 3 * (N-2)/(N-1) * (1-p0)**2 * p0 + (N-3)/(N-1) * (1-p0)**3

def major_incorrect_symbol():
	return 1 - major_correct_symbol() - no_major_symbol()

def fail_all_major_correct():
	return major_correct_symbol()**M * at_least_one_correct_CRC() - prob_CRC_pass()

def fail_one_symbol_lookup():
	return M * major_correct_symbol()**(M-1) * no_major_symbol() * at_least_one_correct_CRC()

def fail_two_symbol_lookup():
	return M * (M - 1) / 2 * major_correct_symbol()**(M-2) * (no_major_symbol())**2 * at_least_one_correct_CRC()

def unrecover():
	return  1 - at_least_one_correct_CRC() + major_incorrect_symbol()

print(major_incorrect_symbol())
# print(no_major_symbol())
# print(1-major_correct_symbol())
# print(at_least_one_correct_CRC() * prob_no_CRC_pass())
print(prob_CRC_pass())
print(fail_all_major_correct())
print(fail_one_symbol_lookup())
print(fail_two_symbol_lookup())
print(unrecover())
print(check_all())
