# RSA Side-Channel Educational Lab

A from-scratch RSA implementation used to **simulate side-channel attacks and measure the effectiveness of standard countermeasures** — timing analysis, simple power analysis (SPA), constant-time exponentiation, the Montgomery ladder, and RSA blinding.

This is not a cryptography library. It is a lab for demonstrating *why* naive modular exponentiation leaks the private exponent, and how real-world libraries (OpenSSL, BoringSSL, etc.) defend against it.

## What it demonstrates

**The vulnerability** — `modexp_vuln` is a textbook square-and-multiply implementation: it only executes the multiply step when the current exponent bit is `1`. That data-dependent branch is exactly what timing and power side-channels exploit.

**Two independent attack simulations:**
- **Timing analysis** (`timing_simulator.py`) — measures wall-clock execution time over many samples to show the vulnerable implementation's timing correlates with the secret exponent, while the hardened implementation does not.
- **Simple power analysis** (`power_simulator.py`) — simulates power traces using a Hamming-weight leakage model with Gaussian noise, the standard technique for modeling SPA/DPA without physical hardware.

**Three countermeasures, implemented and benchmarked against the attacks:**
- `modexp_always` — constant-time exponentiation using arithmetic masking (both branches are always computed; the result is selected algebraically instead of with an `if`).
- `modexp_ladder` — the Montgomery ladder, which performs the same operations in the same order regardless of the exponent bit.
- `blinding.py` — message blinding (`m -> m·r^e mod n`) and exponent blinding (`d -> d + k·φ(n)`), the technique OpenSSL uses by default to defeat timing attacks.

## Measured results

The included run (1024-bit keys, 300 timing samples, 150 power traces) shows the vulnerable and constant-time paths are trivially distinguishable by timing alone:

| Implementation | Mean time (1024-bit key) |
| --- | --- |
| `modexp_vuln` (vulnerable) | ~7.2 ms |
| `modexp_always` (constant-time) | ~10.1 ms |

Full data and charts: [`results/timing_results.csv`](results/timing_results.csv), [`results/timing_histogram.png`](results/timing_histogram.png), [`results/power_mean_traces.csv`](results/power_mean_traces.png).

## Project layout

```text
src/rsa_lab/
├── rsa_primitives.py       # Keypair generation, encrypt/decrypt
├── math_utils.py           # Modular arithmetic helpers
├── modexp_vulnerable.py    # Square-and-multiply (leaky)
├── modexp_constant.py      # Constant-time + Montgomery ladder
├── blinding.py             # Message and exponent blinding
├── timing_simulator.py     # Timing side-channel harness
├── power_simulator.py      # Simulated power-trace (SPA) harness
├── metrics.py / analysis.py
scripts/
├── run_timing_experiment.py
├── run_power_experiment.py
├── run_all_experiments.py  # Runs both, exports CSV + PNG to results/
└── run_presentation_demo.py
tests/
└── test_correctness.py     # Encrypt -> constant-time decrypt round-trip
```

## Running it

```bash
pip install -r requirements.txt
python scripts/run_all_experiments.py   # regenerates results/*.csv and *.png
pytest                                   # correctness round-trip test
```

## Scope

Educational simulation only — key sizes, sample counts, and the power-trace noise model are tuned for demonstrating the effect clearly, not for reproducing a lab-grade hardware attack. Not intended for use as a production cryptography library.
