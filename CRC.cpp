#include <iostream>
#include <string>

using namespace std;

string xorOperation(string a, string b) {
    string res = "";
    for (int i = 1; i < b.length(); i++) {
        if (a[i] == b[i]) {
            res += '0';
        } else {
            res += '1';
        }
    }
    return res;
}

string divide(string data, string key) {
    int keyLen = key.length();
    string temp = data.substr(0, keyLen);
    int dataLen = data.length();

    for (int i = keyLen; i <= dataLen; i++) {
        if (temp[0] == '1') {
            temp = xorOperation(key, temp);
        } else {
            string zeros = "";
            for (int j = 0; j < keyLen; j++) {
                zeros += '0';
            }
            temp = xorOperation(zeros, temp);
        }

        if (i < dataLen) {
            temp += data[i];
        }
    }

    return temp;
}

int main() {
    string msg, key, recMsg;

    cout << "Enter Data Bits: ";
    cin >> msg;
    cout << "Enter Key: ";
    cin >> key;

    string zeros = "";
    for (int i = 0; i < key.length() - 1; i++) {
        zeros += '0';
    }

    string paddedData = msg + zeros;
    string rem = divide(paddedData, key);
    string finalMsg = msg + rem;

    cout << "CRC Remainder: " << rem << endl;
    cout << "Transmitted Codeword: " << finalMsg << endl << endl;

    cout << "Enter Received Data: ";
    cin >> recMsg;

    string recRem = divide(recMsg, key);
    cout << "Receiver Remainder: " << recRem << endl;

    bool flag = false;
    for (int i = 0; i < recRem.length(); i++) {
        if (recRem[i] == '1') {
            flag = true;
            break;
        }
    }

    if (flag) {
        cout << "Result: Error detected!" << endl;
    } else {
        cout << "Result: No error found." << endl;
    }

    return 0;
}
