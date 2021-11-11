from numpy import log2

from c_types import size_t


def count_hx(x):
    res = 0
    p = {}

    for c in x:
        if c not in p:
            p[c] = 1
        else:
            p[c] += 1

    for key, value in p.items():
        p[key] = value / len(x)
        res -= p[key] * log2(p[key])

    return res


def count_hxx(x):
    res = 0
    p = {}
    p_pair = {}

    p[x[0]] = 1

    n = size_t(len(x))
    for i in range(1, n):
        c = x[i]
        prev_c = x[i -1]
        if c not in p:
            p[c] = 1
        else:
            p[c] += 1

        if (c, prev_c) not in p_pair:
            p_pair[(c, prev_c)] = 1
        else:
            p_pair[(c, prev_c)] += 1

    for key, value in p_pair.items():
        key_cur, key_prev = key

        p_pair[key] = value / p[key_prev]
        res -= (p[key_prev] / len(x)) * p_pair[key] * log2(p_pair[key])

    return res


def count_hxxx(x):
    res = 0
    p = {}
    p_pair = {}

    p[(x[1], x[0])] = 1
    p[(x[2], x[1])] = 1

    n = len(x)
    for i in range(2, n):
        cp = (x[i], x[i-1])
        cpp = (x[i], x[i-1], x[i-2])

        if cp not in p:
            p[cp] = 1
        else:
            p[cp] += 1

        if cpp not in p_pair:
            p_pair[cpp] = 1
        else:
            p_pair[cpp] += 1

    for key, value in p_pair.items():
        key_cur, key_p, key_pp = key

        p_pair[key] = value / p[(key_p, key_pp)]
        res -= (p[(key_p, key_pp)] / (len(x) - 2)) * p_pair[key] * log2(p_pair[key])

    return res
