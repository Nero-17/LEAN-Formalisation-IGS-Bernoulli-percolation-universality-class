"""Replay the new descending packed stream against the original initial mass.

This is an implementation cross-check, not a substitute for the Lean proof.
"""
from pathlib import Path
import json
import sys
import time

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[1]


def verify(folder):
    start = time.monotonic()
    data = json.loads((ROOT / "supplementary" / "section5" / "certificates" /
                       folder / "word_base.json").read_bytes())
    depth = data["candidate"]["n"]
    bits = 6 * (depth + 1) + 12
    base, mask = 1 << bits, (1 << bits) - 1
    packed = (3139, 1313)
    for _ in range(depth):
        a, b = packed
        packed = (((22 * a + 18 * b) << bits) + 9 * a + 12 * b,
                  ((5 * a + 18 * b) << bits) + 3 * a + 6 * b)
    counts = (base + 1) ** depth
    determinant = 306 * base ** 2 + 180 * base + 18
    states = [(z, remainder, 1, 0, 0, 1)
              for z, remainder in enumerate(data["lex_remainders"]) if remainder]
    mass0 = mass1 = 0
    for current in range(depth, 0, -1):
        first_numerator = (18 * base + 6) * packed[0] - (18 * base + 12) * packed[1]
        second_numerator = (22 * base + 9) * packed[1] - (5 * base + 3) * packed[0]
        assert first_numerator >= 0 and second_numerator >= 0
        assert first_numerator % determinant == second_numerator % determinant == 0
        packed = first_numerator // determinant, second_numerator // determinant
        assert counts % (base + 1) == 0
        counts //= base + 1
        child_depth = current - 1

        def grouped(z):
            if z > child_depth:
                return 0, 0
            return (packed[0] >> (bits * z)) & mask, (packed[1] >> (bits * z)) & mask

        if current == depth:
            for zeros, (first_false, first_true) in enumerate(data["floor_groups"]):
                if zeros:
                    a, b = grouped(zeros - 1)
                    mass0 += first_false * (22 * a + 18 * b)
                    mass1 += first_false * (5 * a + 18 * b)
                a, b = grouped(zeros)
                mass0 += first_true * (9 * a + 12 * b)
                mass1 += first_true * (3 * a + 6 * b)
        next_states = []
        for zeros, remainder, a, b, c, d in states:
            first_count = ((counts >> (bits * (zeros - 1))) & mask) if zeros else 0
            if remainder <= first_count:
                next_states.append((zeros - 1, remainder, 22*a+5*b, 18*a+18*b,
                                    22*c+5*d, 18*c+18*d))
            else:
                if zeros:
                    x, y = grouped(zeros - 1)
                    mass0 += (22*a+5*b)*x + (18*a+18*b)*y
                    mass1 += (22*c+5*d)*x + (18*c+18*d)*y
                remainder -= first_count
                if remainder:
                    next_states.append((zeros, remainder, 9*a+3*b, 12*a+6*b,
                                        9*c+3*d, 12*c+6*d))
        states = next_states
    assert packed == (3139, 1313) and counts == 1
    for zeros, remainder, a, b, c, d in states:
        if zeros == 0 and remainder:
            mass0 += a*3139 + b*1313
            mass1 += c*3139 + d*1313
    assert [mass0, mass1] == data["mass_vector_numerator"]
    return {"folder": folder, "depth": depth,
            "status": "DESCENDING PACKED STREAM MATCHES ORIGINAL INITIAL MASS",
            "seconds": time.monotonic() - start, "packing_bits": bits}


if __name__ == "__main__":
    folders = sys.argv[1:] or ["n424", "n936", "n952", "transcendental"]
    for folder in folders:
        print(json.dumps(verify(folder)), flush=True)
