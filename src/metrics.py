from pathlib import Path
import json
import numpy as np


def calculate_ber(original_bits, recovered_bits):
    """
    计算误比特率 BER。
    """
    original_bits = np.array(original_bits, dtype=np.uint8)
    recovered_bits = np.array(recovered_bits, dtype=np.uint8)

    if len(original_bits) == 0:
        return 0.0

    min_len = min(len(original_bits), len(recovered_bits))

    bit_errors = np.sum(original_bits[:min_len] != recovered_bits[:min_len])
    bit_errors += abs(len(original_bits) - len(recovered_bits))

    return float(bit_errors / len(original_bits))


def calculate_text_match_rate(original_bytes, recovered_bytes):
    """
    计算文本字节级恢复率。
    """
    if len(original_bytes) == 0:
        return 1.0

    min_len = min(len(original_bytes), len(recovered_bytes))

    same = 0
    for i in range(min_len):
        if original_bytes[i] == recovered_bytes[i]:
            same += 1

    return float(same / len(original_bytes))


def save_metrics(
    output_dir,
    snr_db,
    seed,
    modulation,
    channel,
    payload_bits,
    ber,
    fer,
    text_match_rate,
    checksum_pass,
    sync_start_index,
    true_offset=None
):
    """
    保存 results/metrics.json。

    output_dir 由 main.py 传入，通常是项目根目录下的 results 文件夹。
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics = {
        "snr_db": snr_db,
        "seed": seed,
        "modulation": modulation,
        "channel": channel,
        "payload_bits": int(payload_bits),
        "ber": float(ber),
        "fer": float(fer),
        "text_match_rate": float(text_match_rate),
        "checksum_pass": bool(checksum_pass),
        "sync_start_index": int(sync_start_index),
    }

    if true_offset is not None:
        metrics["true_offset"] = int(true_offset)

    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    return metrics