import math
import json   

POLYNOMIAL_BITSTRING = '10001000000100001'
# POLYNOMIAL_BITSTRING = '10010'
POLYNOMIAL_BITSTRING_32 = '100000100110000010001110110110111'

dict_bit_string = {}

def xor(a, b):
    result = []
    if(len(a) < len(b)):
        c = "0"
        c = c.zfill(len(b) - len(a))
        a = c + a
    for i in range(0, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
 
    return ''.join(result)

def hextobin(ini_string):
    # print(ini_string)
    ini_string_len = len(ini_string) - 2
    digits = 4 * ini_string_len
    # print(digits)
    # scale = 16
    # res = bin(int(ini_string, scale))[2:]
    # print(res)
    match digits:
        case 4:
            res = "{0:04b}".format(int(ini_string, 16))
        case 8:
            res = "{0:08b}".format(int(ini_string, 16))
        case 16:
            res = "{0:016b}".format(int(ini_string, 16))
        case 32:
            res = "{0:032b}".format(int(ini_string, 16))
        # TODO, how to deal with 0 padding
        case default:
            res = bin(int(ini_string, 16))[2:].zfill(digits)
            # print(res)
            # res = "{0:#0{1}x}".format(int(ini_string, 16))
    return res

def bintohex(n):
    size = len(n) / 4
    num = int(n, 2)
    hex_num = hex(num)
    # print(hex_num)
    while len(hex_num[2:]) < size:
        hex_num = "0x" + "0" + hex_num[2:]
    return hex_num

def crc_remainder(input_bitstring, initial_filler = '0'):
    # print(input_bitstring)
    input_bitstring = hextobin(input_bitstring)
    polynomial_bitstring = POLYNOMIAL_BITSTRING.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
    input_padded_array = list(input_bitstring + initial_padding)
    # print(input_padded_array)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
            # print(''.join(input_padded_array))
    return bintohex(''.join(input_padded_array)[len_input:])

def crc16(origin_string):
    # print(origin_string)
    if origin_string.find("0x") != -1:
        origin_string = origin_string[2:]
    # print(origin_string)
    data = bytearray.fromhex(origin_string)
    len1 = len(data)
    crc = 0x0000
    for i in range(len1 - 2):
        newByte = data[i]
        for j in range(8):
            if ((crc & 0x8000) >> 8) ^ (newByte & 0x80):
                crc = (crc << 1) ^ 0x1021
            else:
                crc = (crc << 1)
            newByte <<= 1
        # print(hex(crc))
    result = crc ^ data[len1 - 1] ^ (data[len1 - 2] << 8)
    return "0x" + hex(result & 0xffff)[2:].zfill(4)

def crc_check(input_bitstring, check_value):
    """Calculate the CRC check of a string of bits using a chosen polynomial."""
    # input_bitstring = hextobin(input_bitstring)
    # polynomial_bitstring = POLYNOMIAL_BITSTRING.lstrip('0')
    # len_input = len(input_bitstring)
    # check_value = hextobin(check_value)
    # initial_padding = check_value
    # input_padded_array = list(input_bitstring + initial_padding)
    # while '1' in input_padded_array[:len_input]:
    #     cur_shift = input_padded_array.index('1')
    #     for i in range(len(polynomial_bitstring)):
    #         input_padded_array[cur_shift + i] \
    #         = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    # return ('1' not in ''.join(input_padded_array)[len_input:])
    return crc16(input_bitstring) == check_value

def get_crc_error_code(input_bitstring, check_value):
    crc_real = crc16(input_bitstring)
    # print(crc_real + " " + check_value)
    int_val1 = int(crc_real, 16)
    int_val2 = int(check_value, 16)
    xor_result = int_val1 ^ int_val2
    hex_result = hex(xor_result)
    return "0x" + hex_result[2:].zfill(4)

def construct_bit_string(input_bitstring, dist):
    input_bitstring = hextobin(input_bitstring)
    len_input = len(input_bitstring)
    if dist == 1:
        a = "1"
        while(len(a) <= len_input):
            single_bitstring = a.zfill(len_input)
            list_bit_string = []
            if 1 in dict_bit_string.keys():
                list_bit_string = dict_bit_string[1]
            list_bit_string.append(single_bitstring)
            dict_bit_string[1] = list_bit_string
            a += "0"
    elif dist < len_input:
        list_multi_string = []
        for prev_bitstring in dict_bit_string[dist - 1]:
            last_one_position = prev_bitstring.rindex("1")
            for index in range (last_one_position + 1, len_input):
                new_bitstring = prev_bitstring[:index] + "1" + prev_bitstring[index + 1:]
                list_multi_string.append(new_bitstring)
        dict_bit_string[dist] = list_multi_string


# function not in use and crc_table.json is generated with outdated crc16 algorithm
def crc_error_correct(input_bitstring, check_value, dist):
    crc_error_code = get_crc_error_code(input_bitstring, check_value)
    # for num_bits in range (1, dist + 1):
    #     construct_bit_string(input_bitstring, num_bits)
    # # print("CRC error code: " + crc_error_code)
    input_bitstring = hextobin(input_bitstring)
    len_input = len(input_bitstring)
    crc_table = {}
    with open('crc_table.json') as json_file:
        crc_table = json.load(json_file)
    # for num_bits in range (1, dist + 1):
    #     for bit_string in dict_bit_string[num_bits]:
    #         bit_string_crc = crc_remainder(bintohex(bit_string))
    #         list_bitstring_for_crc = []
    #         if bit_string_crc in crc_table.keys():
    #             list_bitstring_for_crc = crc_table[bit_string_crc]  
    #         list_bitstring_for_crc.append(bit_string)
    #         crc_table[bit_string_crc] = list_bitstring_for_crc
    # print(crc_table)
    if crc_error_code not in crc_table.keys():
        print("No candidate correction found within the given number of bit errors")
        return ""
    ans = []
    for correct_bitstring in crc_table.get(crc_error_code):
        candidate_correction = input_bitstring
        for index in range (0, len_input):
            bit = correct_bitstring[index]
            if (bit == '1'):
                if (candidate_correction[index] == '1'):
                    candidate_correction = candidate_correction[:index] + "0" + candidate_correction[index + 1:]
                else:
                    candidate_correction = candidate_correction[:index] + "1" + candidate_correction[index + 1:]
        ans.append(bintohex(candidate_correction))
    return ans

def display_correction(input_bitstring, bit_string_list):
    input_bitstring = hextobin(input_bitstring)
    len_input = len(input_bitstring)
    ans = []
    for correct_bitstring in bit_string_list:
        candidate_correction = input_bitstring
        for index in range (0, len_input):
            bit = correct_bitstring[index]
            if (bit == '1'):
                if (candidate_correction[index] == '1'):
                    candidate_correction = candidate_correction[:index] + "0" + candidate_correction[index + 1:]
                else:
                    candidate_correction = candidate_correction[:index] + "1" + candidate_correction[index + 1:]
        ans.append(bintohex(candidate_correction))
    return ans



