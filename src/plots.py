from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from src.channel_code import encode, decode
from src.modulation import qpsk_modulate, qpsk_demodulate
from src.channel import awgn_channel
from src.metrics import calculate_ber


def plot_constellation(symbols, output_dir):
    """
    绘制 QPSK 星座图，保存到 results/constellation.png。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.scatter(np.real(symbols), np.imag(symbols), s=8)
    plt.xlabel("In-phase")
    plt.ylabel("Quadrature")
    plt.title("QPSK Constellation")
    plt.grid(True)
    plt.savefig(output_dir / "constellation.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_sync_peak(corr_values, output_dir):
    """
    绘制同步相关峰值图，保存到 results/sync_peak.png。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure()
    plt.plot(corr_values)
    plt.xlabel("Symbol Index")
    plt.ylabel("Correlation")
    plt.title("Synchronization Correlation Peak")
    plt.grid(True)
    plt.savefig(output_dir / "sync_peak.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_ber_curve(payload_bits, seed, output_dir):
    """
    绘制 BER-SNR 曲线，保存到 results/ber_curve.png。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    snr_list = [0, 3, 6, 9, 12, 15]
    ber_list = []

    for snr in snr_list:
        encoded_bits = encode(payload_bits)
        tx_symbols = qpsk_modulate(encoded_bits)
        rx_symbols = awgn_channel(tx_symbols, snr, seed)
        rx_bits = qpsk_demodulate(rx_symbols)

        recovered_bits = decode(rx_bits)
        recovered_bits = recovered_bits[:len(payload_bits)]

        ber = calculate_ber(payload_bits, recovered_bits)
        ber_list.append(ber)

    plt.figure()
    plt.semilogy(snr_list, ber_list, marker="o")
    plt.xlabel("SNR (dB)")
    plt.ylabel("BER")
    plt.title("BER-SNR Curve")
    plt.grid(True)
    plt.savefig(output_dir / "ber_curve.png", dpi=300, bbox_inches="tight")
    plt.close()