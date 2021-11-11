from numpy import append
from c_types import size_t, uint8_t

NON_EXISTING_BIT = 2
BIT_IN_BYTE = 8


def count_number_of_bits(number):
    binary = bin(number)[2:]
    return size_t(len(binary))


def write_bit(vector, free_element, bit):
    vector[-1] = vector[-1] | (bit << free_element)
    free_element += size_t(1)

    if free_element == BIT_IN_BYTE:
        vector = append(vector, uint8_t(0))
        free_element = size_t(0)

    return vector, free_element


def read_bit(vector, index, bit):
    if index >= len(vector):
        return NON_EXISTING_BIT, index, bit

    res = vector[index] >> bit & 1
    bit = bit + uint8_t(1)

    if bit == BIT_IN_BYTE:
        bit = 0
        index += 1

    return res, index, bit
