import numpy as np


def awgn_channel(symbols, snr_db, seed):
    """
    AWGN 信道。

    SNR 定义：
    接收端调制符号平均功率 / 复高斯噪声平均功率。
    """
    rng = np.random.default_rng(seed)

    signal_power = np.mean(np.abs(symbols) ** 2)
    snr_linear = 10 ** (snr_db / 10)

    noise_power = signal_power / snr_linear

    noise = np.sqrt(noise_power / 2) * (
        rng.normal(size=symbols.shape) +
        1j * rng.normal(size=symbols.shape)
    )

    return symbols + noise


def add_random_symbol_offset(symbols, seed, max_offset=128):
    """
    在帧前添加随机符号偏移，用于测试同步模块。

    PRD 要求基础系统应能处理 0 到 128 个 QPSK 符号的随机前置偏移。
    """
    rng = np.random.default_rng(seed + 100)

    offset = int(rng.integers(0, max_offset + 1))

    prefix = np.zeros(offset, dtype=np.complex128)

    return np.concatenate([prefix, symbols]), offset