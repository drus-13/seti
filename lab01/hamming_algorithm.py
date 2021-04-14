import socket

ip = "127.0.0.1"
port = 4000
chuck_lenght = 49
check_bits = [i for i in range(1, chuck_lenght + 1) if not i & (i - 1)]
host_name_by_addr = socket.gethostbyaddr(ip)


def chars_to_bin(chars):
    return ''.join([bin(ord(c))[2:].zfill(16) for c in chars])


def list_different_index(data1, data2):
    different_index = []
    for index, binary_chars in enumerate(zip(list(data1), list(data2))):
        if binary_chars[0] != binary_chars[1]:
            different_index.append(index)
    return different_index


def calc_control_bits(binary_data):
    binary_data = empty_control_bits(binary_data)
    value_control_bits = inf_control_bits(binary_data)
    for controlBit, valueBit in value_control_bits.items():
        binary_data = '{0}{1}{2}'.format(binary_data[:controlBit - 1], valueBit, binary_data[controlBit:])
    return binary_data


def block_iterator(binary_data, word_size):
    for i in range(len(binary_data)):
        if not i % word_size:
            yield binary_data[i:i + word_size]


def inf_control_bits(binary_data):
    map_number_control_bits = {i: 0 for i in check_bits}
    for index, value in enumerate(binary_data, 1):
        if int(value):
            binary_chars = list(bin(index)[2:].zfill(8))
            binary_chars.reverse()
            for power in [2 ** int(j) for j, value in enumerate(binary_chars) if int(value)]:
                map_number_control_bits[power] += 1
    for controlBit, count in map_number_control_bits.items():
        map_number_control_bits[controlBit] = 0 if not count % 2 else 1
    return map_number_control_bits


def excluding_control_bits(binary_data):
    data_without_bits = ''
    for index, binary_char in enumerate(list(binary_data), 1):
        if index not in check_bits:
            data_without_bits += str(binary_char)
    return data_without_bits


def getting_control_bits(binary_data):
    control_bits = {}
    for index, value in enumerate(binary_data, 1):
        if index in check_bits:
            control_bits[index] = int(value)
    return control_bits


def fixing_err(encoded_block):
    res = encoded_block
    encoded_control_bits = getting_control_bits(encoded_block)
    control_value = excluding_control_bits(encoded_block)
    control_value = calc_control_bits(control_value)
    control_bits = getting_control_bits(control_value)
    if encoded_control_bits != control_bits:
        incorrect_bits = []
        for encodedControlBit, value in encoded_control_bits.items():
            if control_bits[encodedControlBit] != value:
                incorrect_bits.append(encodedControlBit)
        bit_number = sum(incorrect_bits)
        res = encoded_block[:bit_number - 1]
        res.append(1 - int(encoded_block[bit_number - 1]))
        res += encoded_block[bit_number:]
    return res


def empty_control_bits(binary_data):
    for bit in check_bits:
        binary_data = binary_data[:bit - 1] + '0' + binary_data[bit - 1:]
    return binary_data


def encode_to_hamming(data):
    bin_data = chars_to_bin(data)
    res = ''
    for binary_block in block_iterator(bin_data, chuck_lenght):
        binary_block = calc_control_bits(binary_block)
        res += binary_block
    return res


def hamming_decode(encoded, fixing_errors=True):
    decoded_data = ''
    encoded_without_error = []
    for enc_block in block_iterator(encoded, chuck_lenght + len(check_bits)):
        if fixing_errors:
            enc_block = fixing_err(enc_block)
        encoded_without_error.append(enc_block)
    corr_block_list = []
    corr_block_str = ""
    for enc_block in encoded_without_error:
        enc_block = excluding_control_bits(enc_block)
        corr_block_list.append(enc_block)
        corr_block_str += enc_block
    for corrChar in [corr_block_str[i:i + 16] for i in range(len(corr_block_str)) if not i % 16]:
        decoded_data += chr(int(corrChar, 2))
    return decoded_data


def recv_all(conn):
    data = b''
    buf_size = 40960
    while True:
        packet = conn.recv(buf_size)
        data += packet
        if len(packet) < buf_size:
            break
    return data



