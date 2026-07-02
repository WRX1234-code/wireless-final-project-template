# DESIGN.md

# Wireless Communication Final Project Design

## 1. Project Overview

This project implements an end-to-end wireless communication baseband simulation system. The objective is to transmit the teacher-provided `Test.txt` through a complete wireless communication chain and finally recover the original text as `results/received.txt`.

The complete communication chain implemented in this project is:

Test.txt → Source Encode → Encrypt / Scramble → Channel Encode → Frame Build → QPSK Modulate → AWGN Channel → Synchronization → QPSK Demodulate → Channel Decode → Decrypt / Descramble → Source Decode → received.txt → Metrics.

The system follows the project PRD and supports command-line execution, fixed random seed, metrics generation, and visualization.

---

## 2. System Architecture

The program adopts a modular design. The main program is `main.py`, which only controls the execution order of each module. All communication algorithms are implemented in the `src` directory.

The main modules are:

- Source Encode
- Encrypt / Scramble
- Channel Encode
- Frame Build
- QPSK Modulate
- AWGN Channel
- Synchronization
- QPSK Demodulate
- Channel Decode
- Decrypt / Descramble
- Source Decode
- Metrics
- Plots

Each module is implemented independently, making the code easy to understand, test and maintain.

---

## 3. Source Encode

The Source Encode module converts UTF-8 text into a binary bit stream. Every byte is converted into eight bits while keeping the original byte order.

The Source Decode module performs the reverse operation. It converts the recovered bit stream back into UTF-8 bytes and writes the recovered text into `results/received.txt`.

To prevent decoding errors caused by QPSK padding, the original payload length is stored inside the frame.

---

## 4. Encrypt / Scramble

The system uses XOR scrambling.

A pseudo-random PN sequence is generated using the fixed random seed.

The transmitter performs XOR between every payload bit and the PN sequence.

The receiver generates the same PN sequence and performs XOR again to recover the original data.

Since XOR is reversible, the scrambling process can be completely removed during reception.

---

## 5. Channel Encode

The Channel Encode module uses repetition coding.

Each information bit is repeated three times before transmission.

The Channel Decode module uses majority voting to recover the transmitted bit.

Although repetition coding reduces transmission efficiency, it improves robustness against AWGN noise and is easy to explain during project presentation.

---

## 6. Frame Build

The Frame Build module constructs a complete transmission frame.

Each frame contains four parts:

- Preamble
- Length
- Payload
- Checksum

The Preamble is used by the Synchronization module.

The Length field records the original payload length before scrambling.

The Payload contains the encoded information bits.

The Checksum is used to verify whether the payload is correctly recovered.

After reception, the Frame Parse module extracts these fields and restores the original payload.

---

## 7. QPSK Modulate

The modulation method is QPSK.

Gray mapping is adopted.

The mapping relationship is

00 → (1+j)/√2

01 → (-1+j)/√2

11 → (-1-j)/√2

10 → (1-j)/√2

The average symbol power is normalized to one.

If the payload contains an odd number of bits, one zero bit is padded before modulation.

The receiver removes the padding according to the Length field.

---

## 8. AWGN Channel

The Channel module simulates an AWGN wireless channel.

The SNR is configurable through the command line.

The random seed is fixed to guarantee reproducibility.

The received signal equals the transmitted signal plus complex Gaussian noise.

---

## 9. Synchronization

The Synchronization module detects the frame start by correlating the received signal with the known preamble.

The receiver slides the preamble along the received symbols and calculates the correlation value.

The position with the maximum correlation peak is selected as the synchronization point.

The synchronization result is recorded as `sync_start_index`.

The synchronization peak is visualized in `sync_peak.png`.

---

## 10. QPSK Demodulate

The QPSK Demodulate module performs quadrant decision.

Each received symbol is mapped back into two bits according to its position in the complex plane.

The recovered bit stream is then passed to the Channel Decode module.

---

## 11. Metrics

The Metrics module calculates the communication performance.

The generated metrics include

- BER
- FER
- payload_bits
- checksum_pass
- text_match_rate
- sync_start_index
- SNR
- random seed

The metrics are saved in `results/metrics.json`.

---

## 12. Visualization

The program generates the following figures.

The QPSK constellation figure shows the distribution of received symbols.

The BER-SNR curve illustrates how BER changes as the channel quality changes.

The synchronization peak figure shows the correlation result used by the Synchronization module.

These figures help evaluate the communication performance visually.

---

## 13. Expected Results

When SNR is greater than or equal to 12 dB under an AWGN Channel, the recovered text should be identical to the original Test.txt.

The expected BER is approximately zero.

FER is approximately zero.

The checksum passes successfully.

The recovered text match rate reaches one hundred percent.

The constellation figure should show four obvious clusters corresponding to the four QPSK constellation points.

The synchronization figure should show a clear correlation peak near the true frame start.

---

## 14. Conclusion

This project successfully implements a complete wireless communication baseband simulation system following the required communication chain.

The implementation covers Source Encode, Encrypt, Scramble, Channel Encode, Frame Build, QPSK Modulate, AWGN Channel, Synchronization, QPSK Demodulate, Channel Decode, Source Decode and Metrics.

The modular implementation makes the system easy to understand, debug and extend.