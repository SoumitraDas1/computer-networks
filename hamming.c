#include <stdio.h>
#include <math.h>

int main() {
    int data[100], code[200];
    int m, r = 0, n, i, j, k = 0;
    int error, errorPos = 0;
    printf("Enter number of data bits: ");
    scanf("%d", &m);
    while ((1 << r) < (m + r + 1)) {
        r++;
    }

    n = m + r;
    printf("Enter %d data bits (0 or 1):\n", m);
    for (i = 0; i < m; i++) {
        scanf("%d", &data[i]);
    }
    for (i = 1; i <= n; i++) {
        code[i] = 0;
    }

    for (i = 1; i <= n; i++) {
        if ((i & (i - 1)) != 0) {
            code[i] = data[k++];
        }
    }
    for (i = 0; i < r; i++) {
        int parityPos = 1 << i;
        int parity = 0;

        for (j = 1; j <= n; j++) {
            if (j & parityPos) {
                parity ^= code[j];
            }
        }

        code[parityPos] = parity;
    }

    printf("\nGenerated Hamming code: ");
    for (i = 1; i <= n; i++) {
        printf("%d", code[i]);
    }

    printf("\n\nEnter error position (0 for no error): ");
    scanf("%d", &error);

    if (error >= 1 && error <= n) {
        code[error] ^= 1;

        printf("Code after introducing error: ");
        for (i = 1; i <= n; i++) {
            printf("%d", code[i]);
        }
        printf("\n");
    }
    for (i = 0; i < r; i++) {
        int parityPos = 1 << i;
        int parity = 0;

        for (j = 1; j <= n; j++) {
            if (j & parityPos) {
                parity ^= code[j];
            }
        }

        if (parity) {
            errorPos += parityPos;
        }
    }

    // Correct error
    if (errorPos == 0) {
        printf("No error detected.\n");
    } else {
        printf("Error detected at position: %d\n", errorPos);

        code[errorPos] ^= 1;

        printf("Corrected Hamming code: ");
        for (i = 1; i <= n; i++) {
            printf("%d", code[i]);
        }
        printf("\n");
    }

    return 0;
}
