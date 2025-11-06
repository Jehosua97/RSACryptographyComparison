# src/rsa_lab/modexp_vulnerable.py
def modexp_square_multiply(m: int, d: int, n: int) -> int:
    """Classic square-and-multiply that branches on secret bits (variable-time)."""
    result = 1
    base = m % n
    for bit in bin(d)[2:]:
        result = (result * result) % n            # square
        if bit == '1':                            # data-dependent branch
            result = (result * base) % n          # multiply
    return result
