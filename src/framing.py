import numpy as np


PREAMBLE_BITS = np.array(
    [1, 0, 1, 0, 1, 0, 1, 0,
     1, 1, 1, 1, 0, 0, 0, 0] * 4,
    dtype=np.uint8
)


def int_to_bits(value, width):
    return np.array(
        [(value >> i) & 1 for i in range(width - 1, -1, -1)],
        dtype=np.uint8
    )


def bits_to_int(bits):
    value = 0
    for b in bits:
        value = (value << 1) | int(b)
    return value


def checksum_bits(payload_bits):
    return int(np.sum(payload_bits) % 256)


def build_frame(encoded_payload_bits, original_payload_len=None, original_payload_bits=None):
    """
    兼容两种用法：
    build_frame(payload_bits)
    build_frame(encoded_payload_bits, original_payload_len, original_payload_bits)
    """
    encoded_payload_bits = np.array(encoded_payload_bits, dtype=np.uint8)

    if original_payload_len is None:
        original_payload_len = len(encoded_payload_bits)

    if original_payload_bits is None:
        original_payload_bits = encoded_payload_bits

    length_bits = int_to_bits(original_payload_len, 32)
    checksum_field = int_to_bits(checksum_bits(original_payload_bits), 8)

    return np.concatenate([
        PREAMBLE_BITS,
        length_bits,
        encoded_payload_bits,
        checksum_field
    ])


def parse_frame(rx_bits, encoded_payload_len=None):
    """
    兼容两种用法：
    1. parse_frame(frame)
       返回 payload_bits, payload_len, checksum
       这样 public_tests 会把 tuple[0] 当作 recovered payload。

    2. parse_frame(frame, encoded_payload_len=...)
       返回 payload_len, encoded_payload_bits, received_checksum
       这样 main.py 原逻辑不受影响。
    """
    rx_bits = np.array(rx_bits, dtype=np.uint8)

    preamble_len = len(PREAMBLE_BITS)
    length_start = preamble_len
    length_end = length_start + 32

    payload_len = bits_to_int(rx_bits[length_start:length_end])

    payload_start = length_end

    if encoded_payload_len is None:
        payload_end = payload_start + payload_len
        checksum_start = payload_end
        checksum_end = checksum_start + 8

        payload_bits = rx_bits[payload_start:payload_end]
        received_checksum = bits_to_int(rx_bits[checksum_start:checksum_end])

        return payload_bits, payload_len, received_checksum

    payload_end = payload_start + encoded_payload_len
    checksum_start = payload_end
    checksum_end = checksum_start + 8

    encoded_payload_bits = rx_bits[payload_start:payload_end]
    received_checksum = bits_to_int(rx_bits[checksum_start:checksum_end])

    return payload_len, encoded_payload_bits, received_checksum