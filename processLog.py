START = "-Header-"
LENGTH = "length"
CODEWORD = "Raw"
CHECK = "checksum invalid"


data_word_list = []
fcs_list = []

def readFile():
	with open('log.txt', 'r') as file:
		lines = file.readlines()
	i = 0
	while i < len(lines):
		payload_len = -1
		line = lines[i].strip()
		# print(line)
		if line.find(START) != -1:
			counter = (counter + 1)
		elif line.find(LENGTH) != -1:
			index = line.find(LENGTH) + len(LENGTH) + 2
			payload_len = line[index:]
			# print(payload_len)
		elif line.find(CODEWORD) != -1:
			counter1 = counter1 + 1
			data_word_list.append(line[4:len(line)-4])
			fcs_list.append(line[len(line)-4:])
		elif line.find(CHECK) != -1:
			data_word_list.append("xxxx")
			fcs_list.append("xxxx")
		i += 1
	print(data_word_list)
			
def process():
	return