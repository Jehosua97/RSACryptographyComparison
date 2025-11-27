from rsa_lab.analysis import timing_experiment

if __name__ == "__main__":
    # Ejecuta un experimento rápido sin exportar archivos
    timing_experiment(samples=200, key_bits=1024)
