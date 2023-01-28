from Lora_data import *

class Lora_data_copies:

	def __init__(self, input_data_copies):
		self.copies = input_data_copies
		self.num_copies = len(input_data_copies)
		self.recover_dict = {}

	def crcCheckAll(self):
		for i in range(0, self.num_copies):
			if(self.copies[i].is_correct):
				self.recover_dict[i] = self.copies[i].data_word
				return True
		return False

	def crcRecover(self):
		if (self.crcCheckAll()):
			return
		for i in range(0, self.num_copies):
			# print("Recover based on " + str(i + 1) + " data copy and its FCS")
			lora_data = self.copies[i]
			crc_recover_list = lora_data.crcRecover(self.copies[:i] + self.copies[i+1:])
			# print(crc_recover_list)
			self.recover_dict[i] = crc_recover_list
		# print("xxxxxxxx Recover completed xxxxxxxxxxx")

	def getRecoverAns(self):
		for i in self.recover_dict.keys():
			print("CRC recover of index " + str(i + 1) + " data copy is: ")
			print(self.recover_dict[i])
