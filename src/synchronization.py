import numpy as np

from src.framing import PREAMBLE_BITS
from src.modulation import qpsk_modulate


def synchronize(received_symbols, preamble=None):
    """
    帧同步：
    支持默认 preamble，也支持测试传入 preamble。
    """
    if preamble is None:
        preamble_symbols = qpsk_modulate(PREAMBLE_BITS)
    else:
        preamble_symbols = np.array(preamble, dtype=np.complex128)

    preamble_len = len(preamble_symbols)
    max_start = len(received_symbols) - preamble_len

    if max_start < 0:
        return 0, np.array([])

    corr_values = []

    for i in range(max_start + 1):
        segment = received_symbols[i:i + preamble_len]
        corr = abs(np.vdot(preamble_symbols, segment))
        corr_values.append(corr)

    corr_values = np.array(corr_values)
    start_index = int(np.argmax(corr_values))

    return start_index, corr_values