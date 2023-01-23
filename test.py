from crc_calculation import *
from CRC_table import *
from Lora_data import *
from utility import *

# Construct CRC_TABLE in advance
input_data_bit_len = 32
max_error_bit = 3
# crc_table = CRC_table(input_data_bit_len, max_error_bit)
# crc_table.construct_crc_table()

# TEST CASE
# origin_input_string = "0xdeadbeef"
# single bit error
# corrupt_input_string = "0xdeadbeff"
# double bit crc_error
# corrupt_input_string = "0xdeadbfff"
# three bits error
corrupt_input_string = "0xdeadbe0f"


# print("CRC encode of: " + origin_input_string + " is: " + crc_remainder(origin_input_string))
# print("CRC encode of: " + corrupt_input_string + " is: " + crc_remainder(corrupt_input_string))
# print("Correct input strings from CRC signle bit correction could be: ")
# print(crc_error_correct(corrupt_input_string, "0xc457", 3))

# lora_data = Lora_data("0xdeadbeff", "0xc457")
# # lora_data.getDataBySymbol()
# lora_data_copies = [Lora_data("0xdeadbeef", "0xc457"), Lora_data("0xdeadb00f", "0xc457")]
# lora_data.recoverCopies(lora_data_copies)
# lora_data.crcRecover()
# print(lora_data.crc_error_code)
# print(lora_data_copies[1].symbol_list)
# print(construct_bit_string(8))

###################################################################
# long input message with 20 bytes

# "This is LoRa message"
origin_input_string = "0x54686973206973204C6F5261206D657373616765"
crc_code = crc_remainder(origin_input_string)
print("CRC encode of: " + origin_input_string + " is: " + crc_code)

# "Thit is LoRa messaga"
corrupt_input_string_1 = "0x54686974206973204C6F5261206D657373616761"
# "This it LoRa message"
corrupt_input_string_2 = "0x54686973206974204C6F5261206D657373616765"
# "This is LoRa messagi"
corrupt_input_string_3 = "0x54686973206973204C6F5261206D657373616769"

lora_data = Lora_data(corrupt_input_string_1, crc_code)
# print(lora_data.data_word)
# print(lora_data.symbol_list)
# print(lora_data.crc_error_code)
lora_data_copies = [Lora_data(corrupt_input_string_2, crc_code), Lora_data(corrupt_input_string_3, crc_code)]
# lora_data.recoverCopies(lora_data_copies)
lora_data.crcRecover(lora_data_copies)
