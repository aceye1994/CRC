from crc_calculation import *
from utility import *

SF = 8
zero = "0"
all_zero = zero.zfill(SF)
bit_list = construct_bit_string(SF)

class Lora_data:

	def __init__(self, input_data, input_crc):
		self.need_crc_set = set()
		self.symbol_list = []
		self.data_word = input_data
		self.frame_check_seq = input_crc
		self.is_correct = crc_check(input_data, input_crc)
		self.crc_error_code = bintohex(get_crc_error_code(self.data_word, self.frame_check_seq))
		bit_string = ""
		data_bit_size = len(hextobin(self.data_word))
		# TODO: check whether data word will pad with 0 if its size is not a multiplier of SF
		self.data_symbol_size = int(data_bit_size / SF)
		binary_data_word = hextobin(self.data_word)
		# print(binary_data_word)
		for i in range(0, self.data_symbol_size):
			self.symbol_list.append(bintohex(binary_data_word[i * SF: i * SF + SF]))
		# print(self.symbol_list)

	def display(self):
		print(self.data_word + " " + self.frame_check_seq)

	def recoverCopies(self, lora_copies):
		recover_symbol_list = {}
		list_size = len(lora_copies)
		if list_size == 0:
			raise Exception("Null pointer")
		for i in range(0, list_size):
			if (self.data_symbol_size != lora_copies[i].data_symbol_size):
				raise Exception("Date copies are with inconsistent data len")
		for i in range(0, self.data_symbol_size):
			symbol = self.symbol_list[i]
			record = {}
			record[symbol] = 1;
			max_occurance = 1;
			for copy in lora_copies:
				# print(copy.getDataBySymbol())
				cur_symbol = copy.symbol_list[i]
				# print(cur_symbol)
				if cur_symbol in record.keys():
					record[cur_symbol] += 1
					if max_occurance == 1:
						max_occurance = record[cur_symbol]
						symbol = cur_symbol
					elif symbol == cur_symbol:
						max_occurance = record[cur_symbol]
					else:
						max_occurance = -1
						break
				else:
					record[cur_symbol] = 1
			if max_occurance > 1:
				recover_symbol_list[i] = symbol
			else:
				self.need_crc_set.add(i)
		# print(recover_symbol_list)
		return recover_symbol_list

	def getRecoverType(self):
		if self.is_correct:
			return 0
		else: 
			return len(self.need_crc_set) + 1

	def crcRecover(self, lora_copies):
		if self.is_correct:
			print("CRC passed, no need to recover")
			return
		recover_symbol_list = self.recoverCopies(lora_copies)
		initial_candidate_correction = "0x"
		for i in range(0, self.data_symbol_size):
			if i in recover_symbol_list.keys():
				initial_candidate_correction += recover_symbol_list[i][2:]
			else:
				initial_candidate_correction += self.symbol_list[i][2:]
		# print(initial_candidate_correction)
		self.crc_error_code = bintohex(get_crc_error_code(initial_candidate_correction, self.frame_check_seq))
		if self.crc_error_code == '0x0':
			recover_data_word = [initial_candidate_correction]
			# print("CRC recover of this data word is: ")
			# print(recover_data_word)
			# return recover_data_word
		else:
			bit_string = ""
			result = []
			self.dfs(0, bit_string, result)
			recover_data_word = display_correction(initial_candidate_correction, result)
		# print("CRC recover of this data word is: ")
		# print(recover_data_word)
		return recover_data_word

	def dfs(self, index, path_string, result):
		if index == self.data_symbol_size:
			bit_string_crc = crc_remainder(bintohex(path_string))
			# print(path_string)
			# print(bit_string_crc)
			if bit_string_crc == self.crc_error_code:
				result.append(path_string)
			return
		else:
			if index in self.need_crc_set:
				for symbol_bit_string in bit_list:
					path_string += symbol_bit_string
					# print(path_string)
					self.dfs(index + 1, path_string, result)
					path_string = path_string[:index * SF]
			else: 
				path_string += all_zero
				self.dfs(index + 1, path_string, result)





