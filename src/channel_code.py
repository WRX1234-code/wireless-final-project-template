import numpy as np


def encode(bits):
    """
    信道编码：
    使用重复码 (3,1)。

    例如：
    0 -> 000
    1 -> 111
    """
    bits = np.array(bits, dtype=np.uint8)
    return np.repeat(bits, 3)


def decode(bits):
    """
    信道译码：
    对每 3 个 bit 做多数判决。

    例如：
    111 -> 1
    001 -> 0
    101 -> 1
    """
    bits = np.array(bits, dtype=np.uint8)

    usable_len = (len(bits) // 3) * 3
    bits = bits[:usable_len]

    if usable_len == 0:
        return np.array([], dtype=np.uint8)

    groups = bits.reshape(-1, 3)

    decoded = (np.sum(groups, axis=1) >= 2).astype(np.uint8)

    return decoded