import secrets
import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from .rsa_primitives import generate_keypair
from .modexp_vulnerable import modexp_vuln
from .modexp_constant import modexp_always
from .timing_simulator import measure_times
from .metrics import js_divergence
from .power_simulator import simulate_trace_square_multiply, simulate_trace_always


def timing_experiment(
    samples: int = 200,
    key_bits: int = 1024,
    csv_path: str | None = None,
    png_path: str | None = None,
) -> None:
    """
    Compara tiempos entre exponentiación vulnerable y estilo constante.
    Puede exportar CSV y PNG.
    """
    key = generate_keypair(key_bits)
    n = key.n

    def vuln_call(m: int) -> int:
        return modexp_vuln(m % n, key.d, n)

    def const_call(m: int) -> int:
        return modexp_always(m % n, key.d, n)

    msgs = [secrets.randbelow(n - 1) + 1 for _ in range(samples)]
    t_v = measure_times(vuln_call, msgs)
    t_c = measure_times(const_call, msgs)

    print("VULN mean", t_v.mean(), "stdev", t_v.std())
    print("CONST mean", t_c.mean(), "stdev", t_c.std())
    print("JS divergence", js_divergence(t_v, t_c))

    # CSV export
    if csv_path is not None:
        p = Path(csv_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["index", "t_vulnerable_ns", "t_constant_ns"])
            for i, (a, b) in enumerate(zip(t_v, t_c)):
                w.writerow([i, int(a), int(b)])
        print(f"[timing] CSV saved to {p}")

    # Plot
    plt.figure()
    plt.hist(t_v, bins=50, alpha=0.6, label="vulnerable")
    plt.hist(t_c, bins=50, alpha=0.6, label="constant-time")
    plt.legend()
    plt.title("Timing distributions")
    plt.xlabel("time (ns)")
    plt.ylabel("count")

    # PNG export
    if png_path is not None:
        p = Path(png_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(p, dpi=200, bbox_inches="tight")
        print(f"[timing] PNG saved to {p}")

    plt.show()


def power_experiment(
    noise: float = 1.0,
    traces: int = 100,
    key_bits: int = 1024,
    csv_path: str | None = None,
    png_path: str | None = None,
) -> None:
    """
    Simula trazas de potencia (SPA) vulnerables vs constantes.
    Exporta media de trazas a CSV y gráfica PNG si se pide.
    """
    key = generate_keypair(key_bits)
    n = key.n

    msgs = [secrets.randbelow(n - 1) + 1 for _ in range(traces)]
    tr_v = [simulate_trace_square_multiply(m, key.d, n, noise) for m in msgs]
    tr_c = [simulate_trace_always(m, key.d, n, noise) for m in msgs]

    # Igualar longitud
    L = min(min(len(t) for t in tr_v), min(len(t) for t in tr_c))
    tr_v_cut = np.vstack([t[:L] for t in tr_v])
    tr_c_cut = np.vstack([t[:L] for t in tr_c])

    mean_v = tr_v_cut.mean(axis=0)
    mean_c = tr_c_cut.mean(axis=0)

    # CSV export de trazas medias
    if csv_path is not None:
        p = Path(csv_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["step", "mean_vulnerable", "mean_constant"])
            for i, (a, b) in enumerate(zip(mean_v, mean_c)):
                w.writerow([i, float(a), float(b)])
        print(f"[power] CSV saved to {p}")

    # Plot
    plt.figure()
    plt.plot(mean_v, label="vulnerable mean")
    plt.plot(mean_c, label="constant-time mean")
    plt.legend()
    plt.title("Mean synthetic power traces")
    plt.xlabel("step")
    plt.ylabel("synthetic power (HW + noise)")

    # PNG export
    if png_path is not None:
        p = Path(png_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(p, dpi=200, bbox_inches="tight")
        print(f"[power] PNG saved to {p}")

    plt.show()
