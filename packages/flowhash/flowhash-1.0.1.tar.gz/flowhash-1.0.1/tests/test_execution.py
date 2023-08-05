import sys
import random

sys.path.append('../src/flowhash')

import flowhash


def main():

    # compound main use case test
    def flow_hash_compound_test(address_size: int) -> None:
        flow = None
        try:
            flow = flowhash.FlowHash(address_size, 256, list(range(1 << address_size)))
        except Exception as ex:
            print(f"::: FAIL ::: Creation of FlowHash over range(1 << {address_size}) failed with exception: {ex}")
            return None
        try:
            flow.execute()
        except Exception as ex:
            print(f"::: FAIL ::: Execution of FlowHash over range(1 << {address_size}) failed with exception: {ex}")
            return None
        try:
            flow.execute()
        except Exception as ex:
            print(f"::: FAIL ::: Aditional execution of FlowHash over range(1 << {address_size}) failed with exception: {ex}")
            return None
        print(f"FlowHash over range(1 << {address_size}) executed successfully.")

    # singleton flowhash test (address_size = 0)
    def flow_hash_singleton_test() -> None:
        flow = None
        try:
            flow = flowhash.FlowHash(0, 256, [0])
        except Exception as ex:
            print(f"::: FAIL ::: Creation of singleton FlowHash failed with exception: {ex}")
            return None
        print(str(flow))
        value = None
        try:
            value = flow.execute()
        except Exception as ex:
            print(f"::: FAIL ::: Execution of singleton FlowHash failed with exception: {ex}")
            return None
        print(str(flow))
        print(f"Singleton FlowHash executed successfully with value {value}")

    # flowhash function test
    def flowhash_hash_test(input_length) -> None:
        hash_input = [random.randrange(0, 1 << 256) for _ in [None] * input_length]
        value = None
        try:
            value = flowhash.flowhash(256, hash_input)
        except Exception as ex:
            print(f"::: FAIL ::: flowhash(256, [{input_length}...]) failed with exception: {ex}")
            return None
        print(f"flowhash(256, [{input_length}...]) executed successfully with value {value}")

    # testing body
    print("Testing hash execution...")

    print("\nTesting FlowHash for different address sizes")
    for i in range(8):
        flow_hash_compound_test(i)

    print("\nTesting singleton FlowHash")
    flow_hash_singleton_test()

    print("\nTesting flowhash function")
    flowhash_hash_test(1)
    flowhash_hash_test(7)
    flowhash_hash_test(16)
    flowhash_hash_test(4)
    flowhash_hash_test(2)
    flowhash_hash_test(83)
    flowhash_hash_test(41)


if __name__ == '__main__':
    main()
    sys.exit(0)