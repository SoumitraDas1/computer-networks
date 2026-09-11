#include <stdio.h>
#include <string.h>

int main()
{
    char data[100], div[20], temp[120];
    int n, m, i, j;

    printf("Enter Data: ");
    scanf("%s", data);

    printf("Enter Divisor: ");
    scanf("%s", div);

    n = strlen(data);
    m = strlen(div);

    strcpy(temp, data);
    for (i = 0; i < m - 1; i++)
        temp[n + i] = '0';
    temp[n + m - 1] = '\0';
    for (i = 0; i < n; i++)
    {
        if (temp[i] == '1')
            for (j = 0; j < m; j++)
                temp[i + j] ^= div[j] ^ '0';
    }

    printf("\nCRC: ");
    for (i = n; i < n + m - 1; i++)
        printf("%c", temp[i]);

    printf("\nCodeword: %s", data);
    for (i = n; i < n + m - 1; i++)
        printf("%c", temp[i]);

    return 0;
}
