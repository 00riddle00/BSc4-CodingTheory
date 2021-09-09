
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
    code = _msg
    code_7_bits = []

    for i in range(0, len(code), 7):
        code_7_bits.append(code[i:i+7])

    code_7 = list(map(str_to_int_array, code_7_bits))
    data_4 = []

    for i in range(len(code_7)):
        code7 = code_7[i]

        sum1 = sum([code7[2], code7[4], code7[6], code7[0]]) % 2
        sum2 = sum([code7[2], code7[5], code7[6], code7[1]]) % 2
        sum3 = sum([code7[4], code7[5], code7[6], code7[3]]) % 2

        if sum1 + sum2 + sum3 > 1:
            bad_index = (sum1) ^ (sum2 << 1) ^ (sum3 << 2)
            code_7[i][bad_index-1] = 1 - code_7[i][bad_index-1]

        data_4.append([code_7[i][2]]+code_7[i][4:7])

    correct_msg = ''.join([str(item) for sublist in data_4 for item in sublist])

    return msg_bin_to_string(correct_msg)

def encode(_msg):
    msg_binary = []

    for i in msg:
        msg_binary.append(format(ord(i), '08b'))

    msg_binary = ''.join(msg_binary)

    data_4_chunks = []

    for i in range(0, len(msg_binary), 4):
        data_4_chunks.append(msg_binary[i:i+4])

    data_4 = list(map(str_to_int_array, data_4_chunks))

    encoded_msg = []

    for i in range(len(data_4_chunks)):
        chunk = data_4[i]

        y1 = sum([chunk[0],chunk[1],chunk[3]]) % 2
        y2 = sum([chunk[0],chunk[2],chunk[3]]) % 2
        y4 = sum([chunk[1],chunk[2],chunk[3]]) % 2

        encoded_msg.append([y1,y2] + [chunk[0]] + [y4] + chunk[1:])

    encoded_msg = ''.join([str(item) for sublist in encoded_msg for item in sublist])

    return encoded_msg

# ==========================================================
# Main
# ==========================================================

# Hamming code H(7,4)

distorted_msg_bin = \
"0100110" \
"0000111" \
"1100010" \
"0100100" \
"1001111" \
"0101011" \
"1100111" \
"1011111" \
"0101111" \
"1001011" \
"0100010" \
"0000010" \
"1110110" \
"1001000" \
"1110110" \
"0111001" \
"1100100" \
"0000101" \
"1100111" \
"0010010" \
"1101110" \
"1111101" \
"0000111" \
"1000010"

assert len(distorted_msg_bin) % 7 == 0

decoded_msg = fix_and_decode(distorted_msg_bin)
assert decoded_msg == "geros dienos"
print(decoded_msg)

msg = "geros dienos"
assert len(msg) == 12

encoded_msg_bin = encode(msg)
decoded_msg = fix_and_decode(encoded_msg_bin)
assert decoded_msg == "geros dienos"
print(decoded_msg)
