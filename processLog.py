import time
from Lora_data import *
from Lora_data_copies import *

START = "-Header-"
LENGTH = "length"
CODEWORD = "Raw"
CHECK = "checksum invalid"
TIMESTAMP = "Time"
FCS = "Got"
DELTA = 10
GAP = 1000

class processLog:

	def __init__(self, files):
		self.numOfCopies = len(files)
		self.log = files
		self.data_word_list_copies = []
		self.fcs_list_copies = []
		self.lora_pkt_list = []
		self.recover_lst = []

	def remove(self, string):
		clean_string = ""
		i = 0
		while i < len(string):
			if string[i] != " ":
				if i + 1 < len(string) and string[i + 1] != " ":
					clean_string += string[i:i+2]
					i += 2
				else:
					clean_string += "0" + string[i]
					i += 1
			else:
				i += 1
		# print(clean_string)
		return clean_string

	def readFile(self, filename):
		with open(filename, 'r') as file:
			lines = file.readlines()
		i = 0
		timer = 0
		data_word_list = []
		fcs_list = []
		while i < len(lines):
			payload_len = -1
			line = lines[i].strip()
			# print(line)
			if line.find(CODEWORD) != -1:
				data_word_list.append("0x"+self.remove(line[9:len(line)-5]))
			elif line.find(FCS) != -1:
				if (len(line) != len(FCS) + 5):
					fcs_list.append("xxxx")
				else:
					fcs_list.append("0x"+line[len(line)-4:])
			elif line.find(TIMESTAMP) != -1:
				cur_timer = int(line[6:])
				if timer == 0:
					timer = cur_timer
				else:
					while cur_timer - timer > GAP + DELTA:
						data_word_list.append("xxxx")
						fcs_list.append("xxxx")
						timer += 1000
					timer = cur_timer
			i += 1
		# print(len(data_word_list))
		# print(len(fcs_list))
		# print(data_word_list)
		# print(fcs_list)
		self.data_word_list_copies.append(data_word_list)
		self.fcs_list_copies.append(fcs_list)
				
	def process(self):
		for filename in self.log:
			self.readFile(filename)
		n = len(self.data_word_list_copies[0])
		for i in range(0, n):
			lora_copies_list = []
			for j in range(0, self.numOfCopies):
				data_word = self.data_word_list_copies[j][i]
				fcs = self.fcs_list_copies[j][i]
				# print(data_word)
				# print(fcs)
				if data_word != "xxxx" and fcs != "xxxx":
					lora_copies_list.append(Lora_data(data_word, fcs))
				# print(len(lora_copies_list))
			self.lora_pkt_list.append(Lora_data_copies(lora_copies_list))

	def recoverAll(self):
		self.process()
		recover_time_record = {}
		for lora_pkt in self.lora_pkt_list:
			if lora_pkt.num_copies >= 2:
				# print("here")
				# lora_pkt.display()
				# print(lora_pkt.num_copies)
				st = time.time()
				lora_pkt.crcRecover()
				et = time.time()
				elapsed_time = et - st
				recover_type = lora_pkt.recover_type
				if recover_type in recover_time_record.keys():
					type_tuple = recover_time_record[recover_type]
					avg_time = type_tuple[0]
					frequence = type_tuple[1]
					new_avg_time = (avg_time * frequence + elapsed_time) / (frequence + 1)
					if recover_type == 4:
						new_avg_time = 9999
					recover_time_record[recover_type] = (new_avg_time, frequence + 1)
				else:
					recover_time_record[recover_type] = (elapsed_time, 1)
				continue
			else:
				# print("there")
				# lora_pkt.display()
				# print(lora_pkt.num_copies)
				if 5 in recover_time_record.keys():
					type_tuple = recover_time_record[5]
					frequence = type_tuple[1]
					recover_time_record[5] = (9999, frequence + 1)
				else:
					recover_time_record[5] = (9999, 1)
				# print("More than 2 copies corrupt and get nothing")
			self.recover_lst.append(lora_pkt.getRecoverAns())
		# print(self.recover_lst)
		# print(len(self.recover_lst))
		# print(recover_time_record)
		self.checkRecoveryAll()
		return recover_time_record

	def checkRecoveryAll(self):
		succeed = 0
		failure = 0
		for i in range(0, len(self.recover_lst)):
			recover_msg_map = self.recover_lst[i]
			msg = "hello world: " + str(i)
			hex_msg =  "0x30303020" + msg.encode('utf-8').hex()
			if self.checkRecoveryOne(recover_msg_map, hex_msg):
				succeed += 1
			else:
				failure += 1
				# print(recover_msg_map)
				# print(self.lora_pkt_list[i].recover_type)
				# self.lora_pkt_list[i].display()
			# print(hex_msg)
		print(succeed)
		print(failure)

	def checkRecoveryOne(self, recover_msg_map, hex_msg):
		if (len(recover_msg_map) == 0):
			return False
		for recover_msgs in recover_msg_map.values():
				for recover_msg in recover_msgs:
					# print(recover_msg)
					if recover_msg == hex_msg:
						return True
		return False

	def display(self):
		file1 = open("myfile.txt","w")
		j = 1
		for lora_pkt in self.lora_pkt_list:
			file1.writelines("msg " + str(j) + "\n")
			j += 1
			L = []
			for i in range(0, lora_pkt.num_copies):
				L.append(lora_pkt.copies[i].data_word + " " + lora_pkt.copies[i].frame_check_seq + "\n")
			file1.writelines(L)
			file1.writelines("\n")
		file1.close()
