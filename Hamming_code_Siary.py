# Hamming Code
# Siary Banerjee

def calculate_redundant_bits(m):
    r = 0
    while 2**r < m + r + 1:
        r += 1
    return r

def add_parity_places(data, r):
    j = 0
    k = 0
    result = ""

    for i in range(1, len(data) + r + 1):
        if i == 2**j:
            result += "0"
            j += 1
        else:
            result += data[k]
            k += 1
    return result

def generate_parity_bits(code, r):
    code = list(code)

    for i in range(r):
        position = 2**i
        parity = 0

        for j in range(1, len(code) + 1):
            if j & position:
                parity ^= int(code[j - 1])

        code[position - 1] = str(parity)

    return "".join(code)

def detect_error_position(code, r):
    error_pos = 0

    for i in range(r):
        position = 2**i
        parity = 0

        for j in range(1, len(code) + 1):
            if j & position:
                parity ^= int(code[j - 1])

        error_pos += parity * position

    return error_pos

data = input("Enter data: ")

r = calculate_redundant_bits(len(data))
code = add_parity_places(data, r)
code = generate_parity_bits(code, r)

print("Hamming Code:", code)

received = input("Enter received code: ")
error = detect_error_position(received, r)

if error == 0:
    print("No error")
else:
    print("Error at position:", error)