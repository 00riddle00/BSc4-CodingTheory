
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
    data_12_bits = []
    y_3_bits = []
    z_4_bits = []
    z_last_bit = []

    data = _msg

    for i in range(0, len(data), 12 + 3 + 4 + 1):
        data_12_bits.append(data[i:i+12])
        y_3_bits.append(data[i+12:i+12+3])
        z_4_bits.append(data[i+12+3:i+12+3+4])
        z_last_bit.append(data[12+3+4])

    data_12 = list(map(str_to_int_array, data_12_bits))
    y_3 = list(map(str_to_int_array, y_3_bits))
    z_4 = list(map(str_to_int_array, z_4_bits))
    z_last = list(map(str_to_int_array, z_last_bit))

    for i in range(len(data_12)):
        data12 = data_12[i]
        y3 = y_3[i]
        z4 = z_4[i]
        zlast = z_last[i]

        row1 = (sum(data12[:4]) + y3[0]) % 2
        row2 = (sum(data12[4:8]) + y3[1]) % 2
        row3 = (sum(data12[8:12]) + y3[2]) % 2

        col1 = sum([data12[0], data12[4], data12[8], z4[0]]) % 2
        col2 = sum([data12[1], data12[5], data12[9], z4[1]]) % 2
        col3 = sum([data12[2], data12[6], data12[10], z4[2]]) % 2
        col4 = sum([data12[3], data12[7], data12[11], z4[3]]) % 2

        last_row_col = (sum(y3[0:3]) + sum(z4[0:4]) + zlast[0]) % 2

        for k,row in enumerate([row1,row2,row3]):
            if row == 1:
                for l,col in enumerate([col1,col2,col3,col4]):
                    if col == 1:
                        data_12[i][4*k+l] = 1 - data_12[i][4*k+l]
                        break
                break

    correct_msg = ''.join([str(item) for sublist in data_12 for item in sublist])

    return msg_bin_to_string(correct_msg)

def encode(_msg):
    msg_binary = []

    for i in msg:
        msg_binary.append(format(ord(i), '08b'))

    # fill 4 bits with "LF" char
    msg_binary += "0110"

    msg_binary = ''.join(msg_binary)

    data_12_chunks = []

    for i in range(0, len(msg_binary), 12):
        data_12_chunks.append(msg_binary[i:i+12])

    data_12 = list(map(str_to_int_array, data_12_chunks))

    encoded_msg = []

    for i in range(len(data_12_chunks)):
        chunk = data_12[i]

        y1 = sum(chunk[:4]) % 2
        y2 = sum(chunk[4:8]) % 2
        y3 = sum(chunk[8:12]) % 2
        z1 = sum([chunk[0], chunk[4], chunk[8]]) % 2
        z2 = sum([chunk[1], chunk[5], chunk[9]]) % 2
        z3 = sum([chunk[2], chunk[6], chunk[10]]) % 2
        z4 = sum([chunk[3], chunk[7], chunk[11]]) % 2
        z_last = sum([y1, y2, y3, z1, z2, z3, z4]) % 2

        encoded_msg.append(chunk + [y1,y2,y3,z1,z2,z3,z4,z_last])

    encoded_msg = ''.join([str(item) for sublist in encoded_msg for item in sublist])

    return encoded_msg

# ==========================================================
# Main
# ==========================================================

# Rectangular Code

# Rec(m,n) = Rec(3,4)
# m - rows
# n - columns

# structure: 12 msg chars, then 8 code chars
# max 1 error per each block of 12 msg chars
distorted_msg_bin = \
"01101111011101101100" \
"00100111100111010000" \
"01101100011001011100" \
"00010111000111001010" \
"00100000011010101010" \
"00100110000100100010" \
"01101100011001011100" \
"01100111010111001100" \
"01101011011000011110"

assert len(distorted_msg_bin) % (12+3+4+1) == 0

decoded_msg = fix_and_decode(distorted_msg_bin)
assert decoded_msg == "grynas vanduo"
print(decoded_msg)

msg = "grynas vanduo"

assert len(msg) == 13

encoded_msg_bin = encode(msg)
decoded_msg = fix_and_decode(encoded_msg_bin)
assert decoded_msg == "grynas vanduo"
print(decoded_msg)
