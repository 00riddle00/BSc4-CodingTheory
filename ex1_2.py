
# ==========================================================
# Helper functions
# ==========================================================

def msg_bin_to_string(msg_bin):
    msg_split_8_bits = [msg_bin[i:i + 8] for i in range(0, len(msg_bin), 8)]
    _msg = []

    for m in msg_split_8_bits:
        char = chr(int(m, 2))
        _msg.append(char)

    return ''.join(_msg)

def str_to_int_array(_str):
    return [int(num) for num in _str]

# ==========================================================
# Main functions
# ==========================================================

def fix_and_decode(_msg):
    data_6_bits = []
    y_4_bits = []

    data = _msg

    for i in range(0, len(data), 6 + 4):
        data_6_bits.append(data[i:i+6])
        y_4_bits.append(data[i+6:i+6+4])

    data_6 = list(map(str_to_int_array, data_6_bits))
    y_4 = list(map(str_to_int_array, y_4_bits))

    sum_elems = [
        [0,1,2], # sum1
        [2,3,4], # sum2
        [1,4,5], # sum3
        [0,3,5], # sum4
    ]

    for i in range(len(data_6)):
        data6 = data_6[i]
        y4 = y_4[i]

        sum1 = (sum(data6[:3]) + y4[0]) % 2
        sum2 = sum([data6[2], data6[3], data6[4], y4[1]]) % 2
        sum3 = sum([data6[1], data6[4], data6[5], y4[2]]) % 2
        sum4 = sum([data6[0], data6[3], data6[5], y4[3]]) % 2

        list_of_sums = [sum1,sum2,sum3,sum4]

        for k,sum1 in enumerate(list_of_sums):
            if sum1 == 1:
                for l,sum2 in enumerate(list_of_sums):
                    if l == k:
                        continue
                    elif sum2 == 1:
                        bad_bit_index = list(set(sum_elems[k]).intersection(sum_elems[l]))
                        assert len(bad_bit_index) == 1
                        bad_bit_index = bad_bit_index[0]

                        data_6[i][bad_bit_index] = 1 - data_6[i][bad_bit_index]
                        break
                break

    correct_msg = ''.join([str(item) for sublist in data_6 for item in sublist])

    return msg_bin_to_string(correct_msg)

def encode(_msg):
    msg_binary = []

    for i in msg:
        msg_binary.append(format(ord(i), '08b'))

    msg_binary = ''.join(msg_binary)

    data_6_chunks = []

    for i in range(0, len(msg_binary), 6):
        data_6_chunks.append(msg_binary[i:i+6])

    data_6 = list(map(str_to_int_array, data_6_chunks))

    encoded_msg = []

    for i in range(len(data_6_chunks)):
        chunk = data_6[i]

        y1 = sum(chunk[:3]) % 2
        y2 = sum([chunk[2],chunk[3],chunk[4]]) % 2
        y3 = sum([chunk[1],chunk[4],chunk[5]]) % 2
        y4 = sum([chunk[0],chunk[3],chunk[5]]) % 2

        encoded_msg.append(chunk + [y1,y2,y3,y4])

    encoded_msg = ''.join([str(item) for sublist in encoded_msg for item in sublist])

    return encoded_msg

# ==========================================================
# Main
# ==========================================================

# Triangular code

# Tr(m) = Tr(3)

# structure: 6 msg chars, then 4 code chars
# max 1 error per each block of 6 msg chars
distorted_msg_bin = \
"0110010111" \
"1101110000" \
"0101001100" \
"1000100101" \
"0010110011" \
"1101111011" \
"0011001101" \
"1000001011" \
"0110011101" \
"0011100011" \
"1001010111" \
"1000011111" \
"0110010011" \
"1001101110" \
"1110011001" \
"0100110110"

assert len(distorted_msg_bin) % (6+4) == 0

decoded_msg = fix_and_decode(distorted_msg_bin)
assert decoded_msg == "geros dienos"
print(decoded_msg)

msg = "geros dienos"
assert len(msg) == 12

encoded_msg_bin = encode(msg)
decoded_msg = fix_and_decode(encoded_msg_bin)
assert decoded_msg == "geros dienos"
print(decoded_msg)
