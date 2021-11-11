from numpy import append, array, delete

from bit_utils import count_number_of_bits, read_bit, write_bit, NON_EXISTING_BIT

from c_types import byte, size_t, uint8_t, uint16_t


def monotone_encode(s, progress_bar=None, whole_status=None):
    if progress_bar is not None:
        progress_bar.set_description(desc='Monotone: Allocating memory...', refresh=True)
        progress_bar.update(whole_status * 0.1)

    result = array([0], dtype=byte)
    free_element = uint8_t(0)

    if progress_bar is not None:
        progress_bar.set_description(desc='Monotone: Encoding...', refresh=True)
        progress_bar.update(whole_status * 0.2)

    for i in range(len(s)):
        current = uint16_t(s[i]) + uint16_t(1)

        number_of_bits = count_number_of_bits(current)

        j = 0
        while j + 1 < number_of_bits:
            result, free_element = write_bit(result, free_element, size_t(1))
            j += 1
        result, free_element = write_bit(result, free_element,  size_t(0))

        j = 1
        while j < number_of_bits:
            bit = size_t((current >> (number_of_bits - size_t(j) - size_t(1))) & size_t(1))
            result, free_element = write_bit(result, free_element, bit)
            j += 1

        if progress_bar is not None:
            progress_bar.update(whole_status * 0.7 / len(s))

    while free_element != 0:
        result, free_element = write_bit(result, free_element, size_t(1))

    result = delete(result, [len(result) - 1])
    return result


def monotone_decode(s, progress_bar=None, whole_status=None):
    if progress_bar is not None:
        progress_bar.set_description(desc='Monotone: Allocating memory...', refresh=True)
        progress_bar.update(whole_status * 0.1)

    result = array([], dtype=byte)
    current_bit = uint8_t(0)
    current_element = 0

    if progress_bar is not None:
        progress_bar.set_description(desc='Monotone: Decoding...', refresh=True)
        progress_bar.update(whole_status * 0.2)

    while True:
        len = uint8_t(0)

        last, current_element, current_bit = read_bit(s, current_element, current_bit)
        while last == 1:
            len += 1
            last, current_element, current_bit = read_bit(s, current_element, current_bit)

        if last == NON_EXISTING_BIT:
            if progress_bar is not None:
                progress_bar.update(whole_status * 0.7)
            return result

        c = uint8_t(1 << len)
        for i in range(1, len + 1):
            last, current_element, current_bit = read_bit(s, current_element, current_bit)
            c |= last << (len - i)

        result = append(result, c - 1)
