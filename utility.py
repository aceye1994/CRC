#utility.py

bit_dict = {}
bit_list = []

def construct_bit_string(symbol_factor):
    a = "1"
    while(len(a) <= symbol_factor):
        single_bitstring = a.zfill(symbol_factor)
        bit_list.append(single_bitstring)
        list_bit_string = []
        if 1 in bit_dict.keys():
            list_bit_string = bit_dict[1]
        list_bit_string.append(single_bitstring)
        bit_dict[1] = list_bit_string
        a += "0"
    for num_bits in range(2, symbol_factor + 1):
        list_multi_string = []
        for prev_bitstring in bit_dict[num_bits - 1]:
            last_one_position = prev_bitstring.rindex("1")
            for index in range (last_one_position + 1, symbol_factor):
                new_bitstring = prev_bitstring[:index] + "1" + prev_bitstring[index + 1:]
                list_multi_string.append(new_bitstring)
                bit_list.append(new_bitstring)
        bit_dict[num_bits] = list_multi_string
    return bit_list
