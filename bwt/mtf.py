from numpy import append, array, arange
from c_types import byte, uint8_t


def mtf_encode(s, progress_bar=None, whole_status=None):
    if progress_bar is not None:
        progress_bar.set_description(desc='MTF: Creating alphabet...', refresh=True)
        progress_bar.update(whole_status * 0.1)

    alphabet = arange(256, dtype=uint8_t).tolist()
    result = array([], dtype=byte)

    if progress_bar is not None:
        progress_bar.set_description(desc='MTF: Constructing sequence...', refresh=True)
        progress_bar.update(whole_status * 0.2)

    for c in s:
        index = uint8_t(0)
        for sym in alphabet:
            if sym == c:
                alphabet.remove(sym)
                break
            index += uint8_t(1)
        alphabet.insert(0, uint8_t(c))
        result = append(result, index)
        if progress_bar is not None:
            progress_bar.update(whole_status * 0.7 / len(s))

    return result


def mtf_decode(s,  progress_bar=None, whole_status=None):
    if progress_bar is not None:
        progress_bar.set_description(desc='MTF: Creating alphabet...', refresh=True)
        progress_bar.update(whole_status * 0.1)

    alphabet = arange(256, dtype=uint8_t).tolist()
    result = array([], dtype=byte)


    if progress_bar is not None:
        progress_bar.set_description(desc='MTF: Constructing sequence...', refresh=True)
        progress_bar.update(whole_status * 0.2)

    for c in s:
        index = 0
        for sym in alphabet:
            if index == c:
                prev = uint8_t(sym)
                result = append(result, prev)
                alphabet.remove(sym)
                alphabet.insert(0, prev)
                break
            index += 1
        if progress_bar is not None:
            progress_bar.update(whole_status * 0.7 / len(s))

    return result
