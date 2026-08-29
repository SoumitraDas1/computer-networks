"""
CRC (Cyclic Redundancy Check) - Computer Networks
--------------------------------------------------
Implements CRC generation (sender side) and CRC checking (receiver side)
using binary polynomial division (mod-2 division / XOR based), exactly
as taught in Computer Networks courses (Data Link Layer error detection).

Concepts:
- Sender appends (n-1) zeros to data (where n = length of generator),
  performs XOR division, and appends the remainder (CRC) to the
  original data before sending.
- Receiver performs the same XOR division on the received data
  (data + CRC). If the remainder is all zeros -> no error detected.
  Otherwise -> error detected.
"""


def xor(a, b):
    """Bitwise XOR of two equal-length binary strings."""
    result = []
    for i in range(1, len(b)):
        result.append('0' if a[i] == b[i] else '1')
    return ''.join(result)


def mod2div(dividend, divisor):
    """
    Perform Modulo-2 (XOR) division and return the remainder.
    """
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    # Final division step
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    return tmp


def encode_data(data, key):
    """
    Sender side: Generate CRC and return the full codeword (data + CRC).
    """
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return codeword, remainder


def check_data(received_codeword, key):
    """
    Receiver side: Check if the received codeword has errors.
    Returns True if no error detected, False if error detected.
    """
    remainder = mod2div(received_codeword, key)
    return remainder, all(bit == '0' for bit in remainder)


def introduce_error(codeword, position):
    """
    Utility: flip a bit at the given position to simulate a
    transmission error (for testing purposes).
    """
    codeword = list(codeword)
    codeword[position] = '1' if codeword[position] == '0' else '0'
    return ''.join(codeword)


def main():
    print("=" * 55)
    print(" CRC (Cyclic Redundancy Check) - Sender & Receiver")
    print("=" * 55)

    # ---- Input ----
    data = input("Enter binary data to send (e.g. 1101011011): ").strip()
    key = input("Enter the generator/divisor polynomial (e.g. 1011): ").strip()

    if not set(data) <= {'0', '1'} or not set(key) <= {'0', '1'}:
        print("Error: Data and key must be binary strings (0s and 1s only).")
        return

    # ---- Sender side ----
    codeword, crc = encode_data(data, key)
    print("\n--- SENDER SIDE ---")
    print(f"Original Data      : {data}")
    print(f"Generator (Key)    : {key}")
    print(f"CRC (Remainder)    : {crc}")
    print(f"Transmitted Data   : {codeword}   (data + CRC)")

    # ---- Simulate transmission ----
    choice = input(
        "\nSimulate a transmission error? (y/n): ").strip().lower()
    transmitted = codeword
    if choice == 'y':
        pos = int(input(
            f"Enter bit position to flip (0-{len(codeword)-1}): "))
        transmitted = introduce_error(codeword, pos)
        print(f"Corrupted Data Sent: {transmitted}")

    # ---- Receiver side ----
    remainder, is_correct = check_data(transmitted, key)
    print("\n--- RECEIVER SIDE ---")
    print(f"Received Data      : {transmitted}")
    print(f"Remainder after div: {remainder}")
    if is_correct:
        print("Result             : No error detected. Data is accepted.")
    else:
        print("Result             : Error detected! Data is corrupted/rejected.")


if __name__ == "__main__":
    main()
