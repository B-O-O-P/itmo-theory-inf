from numpy import append, array, arange, copy
from functools import cmp_to_key

from c_types import byte, uint8_t, int32


def bwt(s, progress_bar=None, whole_status=None):
    if progress_bar is not None:
        progress_bar.update(whole_status * 0.1)

    s_ = copy(s)
    n = len(s_)

    if progress_bar is not None:
        progress_bar.set_description(desc='BWT: Allocating indexes...', refresh=True)
        progress_bar.update(whole_status * 0.2)

    indexes = array(arange(0, n), dtype=int32)

    for i in range(n):
        s_ = append(s_, s_[i])

    def compare(i, j):
        for k in range(n):
            current_i = uint8_t(s_[i + k])
            current_j = uint8_t(s_[j + k])

            if current_i != current_j:
                if current_i < current_j:
                    return -1
                else:
                    return 1

        return -1

    if progress_bar is not None:
        progress_bar.set_description(desc='BWT: Sorting indexes...', refresh=True)
        progress_bar.update(whole_status * 0.05)

    indexes = array(sorted(list(indexes), key=cmp_to_key(compare)))

    result = array([], dtype=byte)
    start = int32(0)

    if progress_bar is not None:
        progress_bar.set_description(desc='BWT: Constructing sequence...', refresh=True)
        progress_bar.update(whole_status * 0.35)

    for i in range(n):
        if indexes[i] == 0:
            start = i

        if progress_bar is not None:
            progress_bar.update(whole_status * 0.3 / n)

        result = append(result, s_[indexes[i] + n - 1])

    return result, start


def inverse_bwt(s, start, progress_bar=None, whole_status=None):
    if progress_bar is not None:
        progress_bar.update(whole_status * 0.1)
    n = len(s)

    if progress_bar is not None:
        progress_bar.set_description(desc='Inverse BWT: Allocating indexes...', refresh=True)
        progress_bar.update(whole_status * 0.2)

    indexes = array(arange(0, n))

    def compare(i, j):
        if s[i] < s[j]:
            return -1
        elif s[i] == s[j]:
            return 0
        else:
            return 1

    if progress_bar is not None:
        progress_bar.set_description(desc='Inverse BWT: Sorting indexes...', refresh=True)
        progress_bar.update(whole_status * 0.05)

    indexes = array(sorted(list(indexes), key=cmp_to_key(compare)))

    result = array([], dtype=byte)
    current = int32(start)

    if progress_bar is not None:
        progress_bar.set_description(desc='Inverse BWT: Restoring sequence...', refresh=True)
        progress_bar.update(whole_status * 0.35)

    for i in range(n):
        result = append(result, s[indexes[current]])
        current = indexes[current]

        if progress_bar is not None:
            progress_bar.update(whole_status * 0.3 / n)

    return result
