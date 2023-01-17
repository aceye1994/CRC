from crc_calculation import *
from CRC_table import *

# Construct CRC_TABLE in advance
input_data_bit_len = 32
max_error_bit = 8
crc_table = CRC_table(input_data_bit_len, max_error_bit)
crc_table.construct_crc_table()

# TEST CASE
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
