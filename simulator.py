import random
import time
from crc_calculation import *
from CRC_table import *
from Lora_data import *
from Lora_data_copies import *
from utility import *

origin_data_word = "0x54686973206973204C6F5261206D657373616765"
origin_fcs = crc_remainder(origin_data_word)
c = 3
p0 = 0.95
hex_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

def buildStr(origin_string):
	string_len = len(origin_string)
	send_string = "0x"
	while(len(send_string) < string_len):
		i = len(send_string)
		mc_random = random.random()
		if (mc_random < p0):
			send_string += origin_string[i:i+2]
		else:
			send_string += random.choice(hex_list) + random.choice(hex_list)
	# print("A random string is: ", send_string)
	return send_string

def buildLoraCopies():
	lora_copies_list = []
	while(len(lora_copies_list) < c):
		data_word = buildStr(origin_data_word)
		fcs = buildStr(origin_fcs)
		# print(data_word + " " + fcs)
		lora_copies_list.append(Lora_data(data_word, fcs))
	lora_data_copies = Lora_data_copies(lora_copies_list)
	# lora_data_copies.display()
	return lora_data_copies

def simulateLoraNtimes(n):
	recover_time_record = {}
	for i in range(0, n):
		lora_data_copies_example = buildLoraCopies()
		st = time.time()
		lora_data_copies_example.crcRecover()
		et = time.time()
		elapsed_time = et - st
		recover_type = lora_data_copies_example.recover_type
		if recover_type in recover_time_record.keys():
			type_tuple = recover_time_record[recover_type]
			avg_time = type_tuple[0]
			frequence = type_tuple[1]
			new_avg_time = (avg_time * frequence + elapsed_time) / (frequence + 1)
			recover_time_record[recover_type] = (new_avg_time, frequence + 1)
		else:
			recover_time_record[recover_type] = (elapsed_time, 1)
		print(recover_time_record)
	return recover_time_record
