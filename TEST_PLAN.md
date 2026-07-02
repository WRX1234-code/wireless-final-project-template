# TEST_PLAN.md

# Wireless Communication Final Project Test Plan

## 1. Test Purpose

The purpose of this test plan is to verify that the wireless communication baseband simulation system satisfies all functional requirements in the project specification.

The system should successfully transmit `Test.txt` through the complete communication chain and recover the original file as `results/received.txt`.

The following communication chain is tested throughout the project.

Source Encode → Encrypt / Scramble → Channel Encode → Frame Build → QPSK Modulate → AWGN Channel → Synchronization → QPSK Demodulate → Channel Decode → Source Decode → Metrics.

---

## 2. Test Environment

Operating System:

Windows 11

Programming Language:

Python 3.11

Main Libraries:

- numpy
- matplotlib
- pytest

---

## 3. Unit Test

### Test 1

Verify Source Encode and Source Decode.

Input a UTF-8 text file.

Convert the text into bits.

Recover the bits back into text.

Expected result:

The recovered text should be identical to the original text.

---

### Test 2

Verify Scramble and Descramble.

Generate a random bit stream.

Scramble the bit stream using the fixed random seed.

Descramble the bit stream using the same seed.

Expected result:

The recovered bit stream should be identical to the original bit stream.

---

### Test 3

Verify Channel Encode and Channel Decode.

Encode a random bit stream using repetition coding.

Decode the encoded bit stream using majority voting.

Expected result:

The decoded bits should equal the original bits when no transmission error exists.

---

### Test 4

Verify Frame Build.

Construct a frame using

- Preamble
- Length
- Payload
- Checksum

Expected result:

The generated frame should contain all required fields.

---

### Test 5

Verify QPSK Modulate and QPSK Demodulate.

Test the Gray mapping.

Expected result:

The recovered bits should be identical to the transmitted bits under a noiseless channel.

---

### Test 6

Verify Synchronization.

Add a random symbol offset before transmission.

Expected result:

The Synchronization module should correctly detect the frame start.

---

## 4. Integration Test

Run the complete communication chain.

Command:

```bash
python main.py --input Test.txt --output results/received.txt --snr 12 --seed 2026 --mod qpsk --channel awgn
```

Expected result:

- received.txt is generated.
- metrics.json is generated.
- constellation.png is generated.
- ber_curve.png is generated.
- sync_peak.png is generated.
- BER is close to zero.
- FER is close to zero.
- checksum_pass is true.
- text_match_rate is equal to one.

---

## 5. Robustness Test

Reduce SNR to a low value.

Expected result:

The program should still complete execution.

The communication quality may decrease, but metrics should still be generated correctly.

---

## 6. Public Test

Run

```bash
pytest public_tests -q
```

Expected result:

The project structure, source code, command-line interface and generated outputs satisfy the public tests.

---

## 7. Expected Output

After successful execution, the following files should exist.

results/received.txt

results/metrics.json

results/constellation.png

results/ber_curve.png

results/sync_peak.png

These outputs are used to evaluate the communication performance.