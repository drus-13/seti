from hamming_algorithm import *


def make_error(encoded_data, n):
    nb_blocks = len(encoded_data) // chuck_lenght + 1
    enc_list = [int(i) for i in encoded_data]
    if n == 2:
        for block_number in range(1, nb_blocks // 2 + 1):
            bit_number = 4
            enc_list[(block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number] = 1 - enc_list[
                (block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number]
    if n == 3:
        for block_number in range(1, nb_blocks // 2 + 1):
            for bit_number in range(4, 6):
                enc_list[(block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number] = 1 - enc_list[
                    (block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number]
    if n == 4:
        for block_number in range(1, nb_blocks*3//4+1):
            if block_number <= nb_blocks//4:
                for bit_number in range(4, 7):
                    enc_list[(block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number] = 1 - enc_list[
                        (block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number]
            if block_number > nb_blocks//4 and block_number <= nb_blocks//2:
                for bit_number in range(4, 6):
                    enc_list[(block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number] = 1 - enc_list[
                        (block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number]
            if block_number > nb_blocks // 2 and block_number <= nb_blocks * 3 // 4:
                bit_number = 4
                enc_list[(block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number] = 1 - enc_list[
                    (block_number - 1) * (chuck_lenght + len(check_bits)) + bit_number]
    encoded_data = str(enc_list)
    encoded_str = ''
    for i in encoded_data:
        if i == "0" or i == "1":
            encoded_str += str(i)
    return encoded_str
