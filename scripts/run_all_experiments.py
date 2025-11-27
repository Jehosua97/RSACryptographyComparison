from rsa_lab.analysis import timing_experiment, power_experiment


def main() -> None:
    print("=== Running timing experiment with CSV + PNG export ===")
    timing_experiment(
        samples=300,
        key_bits=1024,
        csv_path="results/timing_results.csv",
        png_path="results/timing_histogram.png",
    )

    print("\n=== Running power (SPA) experiment with CSV + PNG export ===")
    power_experiment(
        noise=1.0,
        traces=150,
        key_bits=1024,
        csv_path="results/power_mean_traces.csv",
        png_path="results/power_mean_traces.png",
    )

    print("\nAll experiments completed. Check the 'results/' directory.")


if __name__ == "__main__":
    main()
