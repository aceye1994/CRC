import math      

POLYNOMIAL_BITSTRING = '10001000000100001'
# POLYNOMIAL_BITSTRING = '10010'
POLYNOMIAL_BITSTRING_32 = '100000100110000010001110110110111'

def xor(a, b):
    result = []
    for i in range(0, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
 
    return ''.join(result)

def hextobin(ini_string):
    ini_string_len = len(ini_string) - 2
    digits = 4 * ini_string_len
    match digits:
        case 4:
            res = "{0:04b}".format(int(ini_string, 16))
        case 8:
            res = "{0:08b}".format(int(ini_string, 16))
        case 16:
            res = "{0:016b}".format(int(ini_string, 16))
        case 32:
            res = "{0:032b}".format(int(ini_string, 16))
        case default:
            res = "{0:064b}".format(int(ini_string, 16))
    return res

def bintohex(n):
    num = int(n, 2)
    hex_num = hex(num)
    return(hex_num)

def crc_remainder(input_bitstring, initial_filler = '0'):
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

def crc_check(input_bitstring, check_value):
    """Calculate the CRC check of a string of bits using a chosen polynomial."""
    polynomial_bitstring = POLYNOMIAL_BITSTRING.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = check_value
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
    return ('1' not in ''.join(input_padded_array)[len_input:])

def get_crc_error_code(input_bitstring, check_value):
    crc_real = crc_remainder(input_bitstring)
    return xor(hextobin(crc_real), hextobin(check_value))

def crc_error_correct(input_bitstring, check_value):
    crc_error_code = bintohex(get_crc_error_code(input_bitstring, check_value))
    # print("CRC error code: " + crc_error_code)
    input_bitstring = hextobin(input_bitstring)
    len_input = len(input_bitstring)
    a = "1"
    crc_table = {}
    while(len(a) <= len_input):
        single_bitstring = a.zfill(len_input)
        single_bitstring_crc = crc_remainder(bintohex(single_bitstring))
        # print(single_bitstring_crc)
        list_single_bitstring = []
        if single_bitstring_crc in crc_table.keys():
            list_single_bitstring = crc_table[single_bitstring_crc]  
        list_single_bitstring.append(single_bitstring)
        crc_table[single_bitstring_crc] = list_single_bitstring
        # print(crc_table)
        a += "0"
    ans = []
    for correct_single_bitstring in crc_table.get(crc_error_code):
        candidate_correction = input_bitstring
        for index in range (0, len_input):
            bit = correct_single_bitstring[index]
            if (bit == '1'):
                if (candidate_correction[index] == '1'):
                    candidate_correction = candidate_correction[:index] + "0" + candidate_correction[index + 1:]
                else:
                    candidate_correction = candidate_correction[:index] + "1" + candidate_correction[index + 1:]
        ans.append(bintohex(candidate_correction))
    return ans

origin_input_string = "0xdeadbeef"
corrupt_input_string = "0xdeadbeff"
print("CRC encode of: " + origin_input_string + " is: " + crc_remainder(origin_input_string))
print("CRC encode of: " + corrupt_input_string + " is: " + crc_remainder(corrupt_input_string))
print("Correct input strings from CRC signle bit correction could be: ")
print(crc_error_correct(corrupt_input_string, "0xc457"))
# print(crc_error_correct("0x28", "0xe"))
# print(xor("0011010011100010", "1010010101101010"))

