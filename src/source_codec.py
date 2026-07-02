import os
import numpy as np


def text_to_bits(input_data):
    """
    Source Encode:
    支持文件路径或直接字符串输入。
    为了兼容 public_tests，本函数只返回 bit 数组。
    """
    if isinstance(input_data, (str, os.PathLike)) and os.path.exists(input_data):
        with open(input_data, "rb") as f:
            data = f.read()
    else:
        data = str(input_data).encode("utf-8")

    bits = []
    for byte in data:
        bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])

    return np.array(bits, dtype=np.uint8)


def read_text_file_to_bits(input_path):
    """
    main.py 使用：
    读取文件，同时返回 bits 和原始 bytes。
    """
    with open(input_path, "rb") as f:
        data = f.read()

    bits = []
    for byte in data:
        bits.extend([(byte >> i) & 1 for i in range(7, -1, -1)])

    return np.array(bits, dtype=np.uint8), data


def bits_to_text(bits, output_path=None):
    """
    Source Decode:
    不传 output_path 时返回 UTF-8 字符串；
    传 output_path 时写入文件并返回 bytes。
    """
    bits = np.array(bits, dtype=np.uint8)

    byte_list = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) < 8:
            break

        value = 0
        for b in byte_bits:
            value = (value << 1) | int(b)
        byte_list.append(value)

    data = bytes(byte_list)

    if output_path is not None:
        with open(output_path, "wb") as f:
            f.write(data)
        return data

    return data.decode("utf-8", errors="ignore")