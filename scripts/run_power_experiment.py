from rsa_lab.analysis import power_experiment

if __name__ == "__main__":
    # Ejecuta un experimento rápido sin exportar archivos
    power_experiment(noise=1.0, traces=100, key_bits=1024)
