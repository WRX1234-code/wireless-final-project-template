# MOCK_TEST_REPORT.md

# Wireless Communication Mock Test Report

## Mock Test 1

### Objective

Verify that Source Encode and Source Decode are reversible.

### Procedure

A UTF-8 text file was converted into a binary bit stream.

The recovered bit stream was decoded back into text.

### Result

The recovered text was identical to the original text.

### Revision

The source codec was modified to support both text strings and file paths because the public tests may directly pass a string instead of a file.

---

## Mock Test 2

### Objective

Verify Frame Build and Frame Parse.

### Procedure

A random payload was used to generate a frame.

The generated frame was parsed immediately.

### Result

The payload length, payload data and checksum were recovered successfully.

### Revision

The build_frame interface was revised to support both a single payload argument and the complete parameter list.

---

## Mock Test 3

### Objective

Verify QPSK Modulate and QPSK Demodulate.

### Procedure

The four Gray mapping symbol pairs were tested.

Noise was not added during this mock test.

### Result

The modulation and demodulation processes were completely reversible.

### Revision

Padding was added automatically when the payload length was odd.

The receiver removes the padding according to the Length field.

---

## Mock Test 4

### Objective

Verify Synchronization.

### Procedure

Random symbol offsets were inserted before the preamble.

The Synchronization module searched for the correlation peak.

### Result

The frame start was successfully detected.

### Revision

The synchronization interface was modified to support an externally provided preamble because this is required by the public tests.

---

## Mock Test 5

### Objective

Verify the complete communication system.

### Procedure

Run the following command.

```bash
python main.py --input Test.txt --output results/received.txt --snr 12 --seed 2026 --mod qpsk --channel awgn
```

### Result

The following files were generated.

results/received.txt

results/metrics.json

results/constellation.png

results/ber_curve.png

results/sync_peak.png

The metrics showed

BER = 0

FER = 0

checksum_pass = true

text_match_rate = 1.0

### Revision

The output path was standardized so that every generated file is saved inside the results directory.

---

## Summary

Five mock tests were completed before the final submission.

Each mock test helped identify implementation problems and improve the modular design.

The final implementation successfully completed the complete communication chain and generated all required outputs.

## Design Risk and Defect Record

During mock testing, one design risk was found. The original interface design was too strict, which created an issue when public tests called functions with fewer parameters.

A second defect was related to Source Encode. The first version only accepted file paths, but the tests may pass direct text strings.

A third issue was related to Synchronization. The first version only used the internal preamble and did not accept an external preamble.

These defects were fixed through revision, update and change of the corresponding module interfaces.