// Hamming Code for Single-Bit Error Detection

#include <iostream>
#include <string>
#include <cmath>

int calculateRedundantBits(int m) {
    int r = 0;
    while (std::pow(2, r) < m + r + 1) {
        r++;
    }
    return r;
}

std::string addParityPlaces(const std::string& data, int r) {
    int j = 0;
    int k = 0;
    std::string result = "";

    for (int i = 1; i <= data.length() + r; i++) {
        if (i == std::pow(2, j)) {
            result += "0";
            j++;
        } else {
            result += data[k];
            k++;
        }
    }
    return result;
}

std::string generateParityBits(std::string code, int r) {
    for (int i = 0; i < r; i++) {
        int position = std::pow(2, i);
        int parity = 0;

        for (int j = 1; j <= code.length(); j++) {
            if (j & position) {
                parity ^= (code[j - 1] - '0');
            }
        }
        code[position - 1] = '0' + parity;
    }
    return code;
}

int detectErrorPosition(const std::string& code, int r) {
    int errorPos = 0;

    for (int i = 0; i < r; i++) {
        int position = std::pow(2, i);
        int parity = 0;

        for (int j = 1; j <= code.length(); j++) {
            if (j & position) {
                parity ^= (code[j - 1] - '0');
            }
        }

        errorPos += parity * position;
    }
    return errorPos;
}

int main() {
    std::string data;
    std::cout << "Enter data: ";
    std::cin >> data;

    int r = calculateRedundantBits(data.length());
    std::string code = addParityPlaces(data, r);
    code = generateParityBits(code, r);

    std::cout << "Hamming Code: " << code << std::endl;

    std::string received;
    std::cout << "Enter received code: ";
    std::cin >> received;

    int error = detectErrorPosition(received, r);

    if (error == 0) {
        std::cout << "No error" << std::endl;
    } else {
        std::cout << "Error at position: " << error << std::endl;
    }

    return 0;
}
