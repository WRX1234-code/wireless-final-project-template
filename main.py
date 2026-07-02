from pathlib import Path
import argparse
import json

from src.source_codec import read_text_file_to_bits, bits_to_text
from src.scrambler import scramble, descramble
from src.channel_code import encode, decode
from src.framing import build_frame, parse_frame, checksum_bits
from src.modulation import qpsk_modulate, qpsk_demodulate
from src.channel import awgn_channel, add_random_symbol_offset
from src.synchronization import synchronize
from src.metrics import calculate_ber, calculate_text_match_rate, save_metrics
from src.plots import plot_constellation, plot_sync_peak, plot_ber_curve


def main():
    parser = argparse.ArgumentParser(
        description="Wireless Communication Baseband Simulation System"
    )

    parser.add_argument("--input", default="Test.txt", help="Input text file, e.g. Test.txt")
    parser.add_argument("--output", default="results/received.txt", help="Output file, e.g. results/received.txt")
    parser.add_argument("--snr", type=float, default=12, help="SNR in dB")
    parser.add_argument("--seed", type=int, default=2026, help="Random seed")
    parser.add_argument("--mod", default="qpsk", help="Modulation type")
    parser.add_argument("--channel", default="awgn", help="Channel type")

    args = parser.parse_args()

    if args.mod.lower() != "qpsk":
        raise ValueError("Basic system only supports QPSK.")

    if args.channel.lower() != "awgn":
        raise ValueError("Basic system only supports AWGN channel.")

    # 项目根目录：main.py 所在目录
    project_root = Path(__file__).resolve().parent

   # 输出路径：默认是 results/received.txt
   # 如果命令行指定 --output，也使用指定路径
    output_path = Path(args.output)

   # 如果是相对路径，就放到项目根目录下
    if not output_path.is_absolute():
       output_path = project_root / output_path

   # results 文件夹就是 output 文件所在的文件夹
    result_dir = output_path.parent
    result_dir.mkdir(parents=True, exist_ok=True)
    # 1. 源编码：文本 -> bitstream
    payload_bits, original_bytes = read_text_file_to_bits(args.input)
    payload_len = len(payload_bits)

    # 2. 扰码
    scrambled_bits = scramble(payload_bits, args.seed)

    # 3. 信道编码
    encoded_bits = encode(scrambled_bits)
    encoded_payload_len = len(encoded_bits)

    # 4. 组帧
    frame_bits = build_frame(
        encoded_payload_bits=encoded_bits,
        original_payload_len=payload_len,
        original_payload_bits=payload_bits
    )

    # 5. QPSK 调制
    tx_symbols = qpsk_modulate(frame_bits)

    # 6. 添加随机前置偏移，测试同步能力
    tx_symbols_with_offset, true_offset = add_random_symbol_offset(
        tx_symbols,
        seed=args.seed,
        max_offset=128
    )

    # 7. AWGN 信道
    rx_symbols = awgn_channel(
        tx_symbols_with_offset,
        snr_db=args.snr,
        seed=args.seed
    )

    # 8. 同步：检测帧起点
    sync_start_index, corr_values = synchronize(rx_symbols)

    # 9. 截取同步后的有效帧
    aligned_symbols = rx_symbols[
        sync_start_index: sync_start_index + len(tx_symbols)
    ]

    # 10. QPSK 解调
    rx_bits = qpsk_demodulate(aligned_symbols)

    # 11. 解析帧
    recovered_payload_len, recovered_encoded_bits, received_checksum = parse_frame(
        rx_bits,
        encoded_payload_len=encoded_payload_len
    )

    # 12. 信道译码
    recovered_scrambled_bits = decode(recovered_encoded_bits)

    # 根据 length 字段去除 padding
    recovered_scrambled_bits = recovered_scrambled_bits[:recovered_payload_len]

    # 13. 解扰
    recovered_payload_bits = descramble(
        recovered_scrambled_bits,
        args.seed
    )

    # 再次确保长度与原始 payload 一致
    recovered_payload_bits = recovered_payload_bits[:payload_len]

    # 14. 源解码：bitstream -> received.txt
    recovered_bytes = bits_to_text(
        recovered_payload_bits,
        output_path
    )

    # 15. 校验
    original_checksum = checksum_bits(payload_bits)
    checksum_pass = bool(original_checksum == received_checksum)

    # 16. 指标计算
    ber = calculate_ber(payload_bits, recovered_payload_bits)
    fer = 0.0 if ber == 0 else 1.0

    match_rate = calculate_text_match_rate(
        original_bytes,
        recovered_bytes
    )

    metrics = save_metrics(
        output_dir=result_dir,
        snr_db=args.snr,
        seed=args.seed,
        modulation=args.mod.lower(),
        channel=args.channel.lower(),
        payload_bits=payload_len,
        ber=ber,
        fer=fer,
        text_match_rate=match_rate,
        checksum_pass=checksum_pass,
        sync_start_index=sync_start_index,
        true_offset=true_offset
    )

    # 17. 生成图表，全部保存到 results/
    plot_constellation(aligned_symbols, result_dir)
    plot_sync_peak(corr_values, result_dir)
    plot_ber_curve(payload_bits, args.seed, result_dir)

    print("Transmission finished.")
    print(f"received.txt saved to: {output_path}")
    print(f"metrics.json saved to: {result_dir / 'metrics.json'}")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()