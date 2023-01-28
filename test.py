import time

from crc_calculation import *
from CRC_table import *
from Lora_data import *
from Lora_data_copies import *
from utility import *

# Construct CRC_TABLE in advance
def test_generate_crc_table():
	print('\n')
	print("****************************************************")
	print("TEST CRC TABLE GENERATE")
	input_data_bit_len = 32
	max_error_bit = 3
	crc_table = CRC_table(input_data_bit_len, max_error_bit)
	crc_table.construct_crc_table()

# TEST CASE
def test_pure_crc_recover():
	print('\n')
	print("****************************************************")
	print("TEST PURE SINGLE CRC STRING RECOVER")
	origin_input_string = "0xdeadbeef"
	# single bit error
	# corrupt_input_string = "0xdeadbeff"
	# double bit crc_error
	# corrupt_input_string = "0xdeadbfff"
	# three bits error
	corrupt_input_string = "0xdeadbe0f"
	print("CRC encode of: " + origin_input_string + " is: " + crc_remainder(origin_input_string))
	print("CRC encode of: " + corrupt_input_string + " is: " + crc_remainder(corrupt_input_string))
	print("Correct input strings from CRC signle bit correction could be: ")
	print(crc_error_correct(corrupt_input_string, "0xc457", 3))

def test_crc_copies_recover():
	print('\n')
	print("****************************************************")
	print("TEST SHORTER CRC MUTILPLE COPIES RECOVERRY")
	lora_data = Lora_data("0xdeadbeff", "0xc457")
	# # lora_data.getDataBySymbol()
	lora_data_copies = [Lora_data("0xdeadbeee", "0xc457"), Lora_data("0xdeadb00f", "0xc457")]
	# lora_data.recoverCopies(lora_data_copies)
	print("CRC recover of this data word is: ")
	print(lora_data.crcRecover(lora_data_copies))
	# print(lora_data.crc_error_code)
	# print(lora_data_copies[1].symbol_list)
	# print(construct_bit_string(8))


# long input message with 20 bytes
def test_crc_copies_recover_long():
	print('\n')
	print("****************************************************")
	print("TEST LONGER CRC MUTILPLE COPIES RECOVERRY")
	# Original data "This is LoRa message"
	origin_input_string = "0x54686973206973204C6F5261206D657373616765"
	crc_code = crc_remainder(origin_input_string)
	print("CRC encode of: " + origin_input_string + " is: " + crc_code)

	# 3 copies all corrupted
	# "Thit is LoRa messaga"
	corrupt_input_string_1 = "0x54686974206973204C6F5261206D657373616761"
	# "This it LoRa message"
	corrupt_input_string_2 = "0x54686973206974204C6F5261206D657373616765"
	# "This is LoRa messagi"
	corrupt_input_string_3 = "0x54686973206973204C6F5261206D657373616769"

	# lora_data = Lora_data(corrupt_input_string_2, crc_code)
	# print(lora_data.data_word)
	# print(lora_data.symbol_list)
	# print(lora_data.crc_error_code)
	# lora_data_copies = [Lora_data(corrupt_input_string_1, crc_code), Lora_data(corrupt_input_string_3, crc_code)]
	lora_data_copies = Lora_data_copies([Lora_data(corrupt_input_string_1, crc_code), Lora_data(corrupt_input_string_2, crc_code), Lora_data(corrupt_input_string_3, crc_code)])
	# lora_data.crcRecover(lora_data_copies)
	# for i in range(0, len(lora_data_copies)):
	# 	print("CRC recover of index " + str(i + 1) + " data copy is: ")
	# 	lora_data = lora_data_copies[i]
	# 	lora_data.crcRecover(lora_data_copies[:i] + lora_data_copies[i+1:])
	lora_data_copies.crcRecover()
	lora_data_copies.getRecoverAns()

def test_time_crc_pass():
	st = time.time()
	origin_input_string = "0x54686973206973204C6F5261206D657373616765"
	crc_code = crc_remainder(origin_input_string)
	# "Thit is LoRa messaga"
	corrupt_input_string_1 = "0x54686974206973204C6F5261206D657373616761"
	corrupt_input_string_2 = origin_input_string
	# "This is LoRa messagi"
	corrupt_input_string_3 = "0x54686973206973204C6F5261206D657373616769"
	lora_data_copies = Lora_data_copies([Lora_data(corrupt_input_string_1, crc_code), Lora_data(corrupt_input_string_2, crc_code), Lora_data(corrupt_input_string_3, crc_code)])
	lora_data_copies.crcRecover()
	# lora_data_copies.getRecoverAns()
	et = time.time()
	elapsed_time = et - st
	print('Execution for one CRC pass:', elapsed_time, 'seconds')

def test_time_major_correct():
	st = time.time()
	origin_input_string = "0x54686973206973204C6F5261206D657373616765"
	crc_code = crc_remainder(origin_input_string)
	# "Thit is LoRa message"
	corrupt_input_string_1 = "0x54686974206973204C6F5261206D657373616765"
	# "This it LoRa message"
	corrupt_input_string_2 = "0x54686973206974204C6F5261206D657373616765"
	# "This is LoRa messagi"
	corrupt_input_string_3 = "0x54686973206973204C6F5261206D657373616769"
	lora_data_copies = Lora_data_copies([Lora_data(corrupt_input_string_1, crc_code), Lora_data(corrupt_input_string_2, crc_code), Lora_data(corrupt_input_string_3, crc_code)])
	lora_data_copies.crcRecover()
	# lora_data_copies.getRecoverAns()
	et = time.time()
	elapsed_time = et - st
	print('Execution for major Correct:', elapsed_time, 'seconds')

def test_time_one_symbol():
	st = time.time()
	origin_input_string = "0x54686973206973204C6F5261206D657373616765"
	crc_code = crc_remainder(origin_input_string)
	# "Thit is LoRa messaga"
	corrupt_input_string_1 = "0x54686974206973204C6F5261206D657373616761"
	# "This it LoRa message"
	corrupt_input_string_2 = "0x54686973206974204C6F5261206D657373616765"
	# "This is LoRa messagi"
	corrupt_input_string_3 = "0x54686973206973204C6F5261206D657373616769"
	lora_data_copies = Lora_data_copies([Lora_data(corrupt_input_string_1, crc_code), Lora_data(corrupt_input_string_2, crc_code), Lora_data(corrupt_input_string_3, crc_code)])
	lora_data_copies.crcRecover()
	# lora_data_copies.getRecoverAns()
	et = time.time()
	elapsed_time = et - st
	print('Execution for one sysmbol:', elapsed_time, 'seconds')

def test_time_two_symbol():
	st = time.time()
	origin_input_string = "0x54686973206973204C6F5261206D657373616765"
	crc_code = crc_remainder(origin_input_string)
	# "Thit is LoRa messaga"
	corrupt_input_string_1 = "0x54686974206973204C6F5261206D657373616761"
	# "This it LoRe message"
	corrupt_input_string_2 = "0x54686973206974204C6F5265206D657373616765"
	# "This is LoRi messagi"
	corrupt_input_string_3 = "0x54686973206973204C6F5269206D657373616769"
	lora_data_copies = Lora_data_copies([Lora_data(corrupt_input_string_1, crc_code), Lora_data(corrupt_input_string_2, crc_code), Lora_data(corrupt_input_string_3, crc_code)])
	lora_data_copies.crcRecover()
	# lora_data_copies.getRecoverAns()
	et = time.time()
	elapsed_time = et - st
	print('Execution for two sysmbol:', elapsed_time, 'seconds')

# test_generate_crc_table()
# test_pure_crc_recover()
# test_crc_copies_recover()
# test_crc_copies_recover_long()
test_time_crc_pass()
test_time_major_correct()
test_time_one_symbol()
test_time_two_symbol()
