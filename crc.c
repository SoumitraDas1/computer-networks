 #include <stdio.h>
#include <string.h>

int main() {
    char data[30], divisor[10], temp[30], quotient[30], remainder[10];
    int data_len, div_len, i, j;

    printf("Enter Data: ");
    scanf("%s", data);

    printf("Enter Divisor: ");
    scanf("%s", divisor);

    data_len = strlen(data);
    div_len = strlen(divisor);

    strcpy(temp, data);

    for (i = 0; i < div_len - 1; i++)
        temp[data_len + i] = '0';

    temp[data_len + div_len - 1] = '\0';

    for (i = 0; i < data_len; i++) {
        quotient[i] = temp[i];

        if (temp[i] == '1') {
            for (j = 0; j < div_len; j++) {
                temp[i + j] = (temp[i + j] == divisor[j]) ? '0' : '1';
            }
        }
    }

    for (i = 0; i < div_len - 1; i++)
        remainder[i] = temp[data_len + i];

    remainder[i] = '\0';

    printf("Remainder (CRC): %s\n", remainder);

    strcat(data, remainder);
    printf("Codeword: %s\n", data);

    return 0;
}