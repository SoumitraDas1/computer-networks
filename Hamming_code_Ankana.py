#Hamming_code
#Ankana_dey

def get_parity_bits(m):
    r = 0
    while 2**r < m + r + 1:
        r += 1
    return r

def insert_bits(data, r):
    j = 0
    k = 0
    res = ""

    for i in range(1, len(data) + r + 1):
        if i == 2**j:
            res += "0"
            j += 1
        else:
            res += data[k]
            k += 1
    return res

def set_parity(code, r):
    code = list(code)

    for i in range(r):
        pos = 2**i
        val = 0

        for j in range(1, len(code)+1):
            if j & pos:
                val ^= int(code[j-1])

        code[pos-1] = str(val)

    return "".join(code)

def find_error(code, r):
    error = 0

    for i in range(r):
        pos = 2**i
        val = 0

        for j in range(1, len(code)+1):
            if j & pos:
                val ^= int(code[j-1])

        error += val * pos

    return error

data = input("Enter data: ")

r = get_parity_bits(len(data))
code = insert_bits(data, r)
code = set_parity(code, r)

print("Hamming Code:", code)

received = input("Enter received code: ")
error = find_error(received, r)

if error == 0:
    print("No error")
else:
    print("Error at position:", error)