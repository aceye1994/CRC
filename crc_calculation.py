import math      

POLYNOMIAL_BITSTRING = '10001000000100001'
POLYNOMIAL_BITSTRING_32 = '100000100110000010001110110110111'

def xor(a, b):
    result = []
    # Traverse all bits, if bits are same, then XOR is 0, else 1
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
 
    return ''.join(result)


def mod2div(dividend, divisor):
    # Number of bits to be XORed at a time.
    pick = len(divisor)
    # Slicing the dividend to appropriate length for particular step
    tmp = dividend[0 : pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            # replace the dividend by the result of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + dividend[pick]
        else: # If leftmost bit is '0'
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)
    checkword = tmp
    return checkword

def encodeData(hex_data, key = "10001000000100001"):
    data = hextobin(hex_data)
    l_key = len(key)
    appended_data = data + '0'*(l_key - 1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return bintohex(remainder)

def hextobin(ini_string):
    res = "{0:016b}".format(int(ini_string, 16))
    return res

def bintohex(n):
    num = int(n, 2)
    hex_num = hex(num)
    return(hex_num)

def crc_remainder(input_bitstring, initial_filler = '0'):
    """Calculate the CRC remainder of a string of bits using a chosen polynomial.
    initial_filler should be '1' or '0'.
    """
    polynomial_bitstring = POLYNOMIAL_BITSTRING.lstrip('0')
    len_input = len(input_bitstring)
    initial_padding = (len(polynomial_bitstring) - 1) * initial_filler
    input_padded_array = list(input_bitstring + initial_padding)
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            input_padded_array[cur_shift + i] \
            = str(int(polynomial_bitstring[i] != input_padded_array[cur_shift + i]))
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

def crc32(data: bytes, poly = 0x04C11DB7):
    '''
    CRC-16-CCITT Algorithm
    '''
    data = bytearray(data)
    crc = 0xFFFFFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFFFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    
    return crc & 0xFFFFFFFF

def crc16(data: bytes, poly=0x1021):
    '''
    CRC-16-CCITT Algorithm
    '''
    data = bytearray(data)
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    return crc & 0xFFFF

print(encodeData("deadbeaf"))
# print(hextobin('0x1021'))
print(crc_remainder(hextobin("deadbeaf")))
print(hex(crc32(b'deadbeaf')))
print(hex(crc16(b'deadbeaf')))
print(bintohex(xor(hextobin(encodeData("deadbe")), hextobin("ef"))))

