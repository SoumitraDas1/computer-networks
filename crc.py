def xor(a, b):
    result = ""
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"
    return result

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    return tmp

# Sender Side
data = input("Enter data bits: ")
generator = input("Enter generator polynomial: ")

appended_data = data + '0' * (len(generator) - 1)
remainder = mod2div(appended_data, generator)

codeword = data + remainder

print("CRC Remainder:", remainder)
print("Transmitted Codeword:", codeword)

# Receiver Side
received = input("Enter received codeword: ")

check = mod2div(received, generator)

if int(check) == 0:
    print("No Error Detected")
else:
    print("Error Detected")