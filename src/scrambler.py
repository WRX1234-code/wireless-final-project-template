import numpy as np


def generate_pn_sequence(length, seed):
    """
    生成 PN 伪随机序列。
    扰码和解扰必须使用同一个 seed，才能保证可逆。
    """
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, length, dtype=np.uint8)


def scramble(bits, seed):
    """
    XOR 扰码：
    scrambled = bits XOR pn_sequence
    """
    pn = generate_pn_sequence(len(bits), seed)
    return np.bitwise_xor(bits, pn)


def descramble(bits, seed):
    """
    XOR 解扰：
    XOR 操作具有自反性，因此解扰和扰码使用同一个函数。
    """
    return scramble(bits, seed)