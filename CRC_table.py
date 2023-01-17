import json
from crc_calculation import *

class CRC_table:

	bit_list = {}
	crc_precomputed_table = {}
	POLYNOMIAL_BITSTRING = '10001000000100001'

	def __init__(self, input_bitstring_bitlen, max_num_bits):
		self.len = input_bitstring_bitlen
		self.bits = max_num_bits

	def construct_list(self):
		for num_bits in range (1, self.bits + 1):
			self.construct_bit_string(num_bits)

	def construct_bit_string(self, num_bits):
	    if num_bits == 1:
	        a = "1"
	        while(len(a) <= self.len):
	            single_bitstring = a.zfill(self.len)
	            list_bit_string = []
	            if 1 in self.bit_list.keys():
	                list_bit_string = self.bit_list[1]
	            list_bit_string.append(single_bitstring)
	            self.bit_list[1] = list_bit_string
	            a += "0"
	    elif num_bits < self.len:
	        list_multi_string = []
	        for prev_bitstring in self.bit_list[num_bits - 1]:
	            last_one_position = prev_bitstring.rindex("1")
	            for index in range (last_one_position + 1, self.len):
	                new_bitstring = prev_bitstring[:index] + "1" + prev_bitstring[index + 1:]
	                list_multi_string.append(new_bitstring)
	        self.bit_list[num_bits] = list_multi_string

	def construct_crc_table(self):
		self.construct_list()
		for num_bits in self.bit_list.keys():
			for bit_string in self.bit_list[num_bits]:
				bit_string_crc = crc_remainder(bintohex(bit_string))
				list_bitstring_for_crc = []
				if bit_string_crc in self.crc_precomputed_table.keys():
				    list_bitstring_for_crc = self.crc_precomputed_table[bit_string_crc]  
				list_bitstring_for_crc.append(bit_string)
				self.crc_precomputed_table[bit_string_crc] = list_bitstring_for_crc
			print("Progress: " + str(num_bits) + " out of " + str(self.bits) + " is done ")
		with open("crc_table.json", "w") as outfile:
   			json.dump(self.crc_precomputed_table, outfile, indent = 4)

