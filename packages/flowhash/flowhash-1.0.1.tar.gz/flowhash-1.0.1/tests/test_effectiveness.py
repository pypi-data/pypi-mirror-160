import sys
import random

sys.path.append('../src/flowhash')

import flowhash


def main():

    # test that patterns do not persist in hash
    def pattern_destruction_test(pattern: list, max: int, modulos: list) -> None:
        hash_modulo_buckets = {modulo: [0] * modulo for modulo in modulos}
        for i in range(0, max):
            mh = flowhash.flowhash(256, pattern * i)
            for modulo in modulos:
                hash_modulo_buckets[modulo][mh % modulo] = hash_modulo_buckets[modulo][mh % modulo] + 1
        for modulo in modulos:
            expected = max / modulo
            chi = sum([(bucket - expected) ** 2 / expected for bucket in hash_modulo_buckets[modulo]])
            print(f"Pattern {pattern} produced distribution {hash_modulo_buckets[modulo]} for modulo {modulo} over {max} iterations. (expected value: {max/modulo})")
            print(f"This sampled distribution has chi-square value {chi} and {modulo - 1} degrees of freedom.")

    # test that the hash is sensitive to changes in the input
    def input_sensitivity_test(varients: int, input_length: int, modulos: list) -> None:
        hash_modulo_buckets = {modulo: [0] * modulo for modulo in modulos}
        base_input = [random.randrange(0, 1 << 256) for _ in [None] * input_length]
        for i in range(0, varients):
            place = random.randrange(0, input_length)
            bit = (1 << random.randrange(0, 256))
            base_input[place] = base_input[place] ^ bit # flip a bit
            mh = flowhash.flowhash(255, base_input)
            for modulo in modulos:
                hash_modulo_buckets[modulo][mh % modulo] = hash_modulo_buckets[modulo][mh % modulo] + 1
            base_input[place] = base_input[place] ^ bit # flip the bit back
        for modulo in modulos:
            expected = varients / modulo
            chi = sum([(bucket - expected) ** 2 / expected for bucket in hash_modulo_buckets[modulo]])
            print(f"Input produced distribution {hash_modulo_buckets[modulo]} for modulo {modulo} over {varients} iterations. (expected value: {varients/modulo})")
            print(f"This sampled distribution has chi-square value {chi} and {modulo - 1} degrees of freedom.")

    # testing body
    print("Testing hash security...")

    #* Efficiency dips after around 128 chunks.

    iters = 64
    mods = [2, 3, 5, 7, 16]

    #! Given the current performance of the hash function...
    #! it is not possible to be confident in any assertions...
    #! of security given by the following pattern destruction tests.
    print("\nPattern Testing")

    pattern_destruction_test([0], iters, mods)
    pattern_destruction_test([255], iters, mods)
    pattern_destruction_test([0, 255], iters, mods)
    pattern_destruction_test([255, 0], iters, mods)

    pattern_destruction_test([1], iters, mods)
    pattern_destruction_test([254], iters, mods)
    pattern_destruction_test([1, 254], iters, mods)
    pattern_destruction_test([254, 1], iters, mods)

    print("\nAssuring anomalies are flukes")

    #! This test should demonstrate the anomaly of [255] is a fluke.
    pattern_destruction_test([255], 2 * iters, mods)

    print("\nSensitivity Testing")

    input_sensitivity_test(iters, 64, mods)
    input_sensitivity_test(iters, 64, mods)
    input_sensitivity_test(iters, 64, mods)
    input_sensitivity_test(iters, 64, mods)

    input_sensitivity_test(iters, 64, mods)
    input_sensitivity_test(iters, 64, mods)
    input_sensitivity_test(iters, 64, mods)
    input_sensitivity_test(iters, 64, mods)


if __name__ == "__main__":
    main()
    sys.exit(0)

