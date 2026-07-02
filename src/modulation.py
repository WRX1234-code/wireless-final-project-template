import numpy as np


def qpsk_modulate(bits):
    """
    QPSK 调制。

    使用 PRD 要求的 Gray 编码映射：

    00 -> (1+j)/sqrt(2)
    01 -> (-1+j)/sqrt(2)
    11 -> (-1-j)/sqrt(2)
    10 -> (1-j)/sqrt(2)

    sqrt(2) 用于功率归一化，使平均符号功率约为 1。
    """
    bits = np.array(bits, dtype=np.uint8)

    # QPSK 每 2 bit 映射为 1 个符号
    # 如果 bit 数不是偶数，则在末尾补 0
    if len(bits) % 2 != 0:
        bits = np.append(bits, 0)

    symbols = []

    for i in range(0, len(bits), 2):
        b1, b2 = bits[i], bits[i + 1]

        if b1 == 0 and b2 == 0:
            symbol = 1 + 1j
        elif b1 == 0 and b2 == 1:
            symbol = -1 + 1j
        elif b1 == 1 and b2 == 1:
            symbol = -1 - 1j
        else:
            symbol = 1 - 1j

        symbols.append(symbol / np.sqrt(2))

    return np.array(symbols, dtype=np.complex128)


def qpsk_demodulate(symbols):
    """
    QPSK 解调。

    使用象限判决恢复 bit。
    """
    bits = []

    for s in symbols:
        real = np.real(s)
        imag = np.imag(s)

        if real >= 0 and imag >= 0:
            bits.extend([0, 0])
        elif real < 0 and imag >= 0:
            bits.extend([0, 1])
        elif real < 0 and imag < 0:
            bits.extend([1, 1])
        else:
            bits.extend([1, 0])

    return np.array(bits, dtype=np.uint8)