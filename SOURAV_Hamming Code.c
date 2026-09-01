/*
 * HAMMING CODE - Error Detection and Correction
 * Computer Networks Lab Program
 * ---------------------------------------------
 * This program:
 *   1. Encodes a given data bit stream using Hamming Code (adds parity bits)
 *   2. Simulates a transmission error (single bit flip)
 *   3. Detects the error position at the receiver
 *   4. Corrects the error and recovers the original data
 *
 * Compile: gcc hamming.c -o hamming
 * Run    : ./hamming
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* ---------- Function Prototypes ---------- */
int calculateParityBits(int dataBits);
void encodeHamming(int data[], int dataBits, int encoded[], int totalBits, int r);
void displayCode(int arr[], int n, const char *msg);
int detectAndCorrect(int received[], int totalBits, int r);

/* ---------------------------------------------------------
   Returns number of redundant (parity) bits required
   using the formula: 2^r >= m + r + 1
--------------------------------------------------------- */
int calculateParityBits(int m) {
    int r = 0;
    while (pow(2, r) < (m + r + 1))
        r++;
    return r;
}

/* ---------------------------------------------------------
   Checks if a position is a power of 2 (i.e., a parity bit)
--------------------------------------------------------- */
int isPowerOfTwo(int x) {
    return (x != 0) && ((x & (x - 1)) == 0);
}

/* ---------------------------------------------------------
   Encodes data bits into Hamming code
--------------------------------------------------------- */
void encodeHamming(int data[], int dataBits, int encoded[], int totalBits, int r) {
    int j = 0; /* index for data[] */

    /* Step 1: Place data bits into non-power-of-2 positions (1-indexed) */
    for (int i = 1; i <= totalBits; i++) {
        if (isPowerOfTwo(i)) {
            encoded[i - 1] = 0; /* placeholder for parity bit */
        } else {
            encoded[i - 1] = data[j++];
        }
    }

    /* Step 2: Calculate each parity bit */
    for (int i = 0; i < r; i++) {
        int parityPos = (int) pow(2, i);
        int count = 0;

        /* Check bits covered by this parity bit */
        for (int pos = 1; pos <= totalBits; pos++) {
            if (pos & parityPos) {
                if (pos != parityPos)
                    count += encoded[pos - 1];
            }
        }
        encoded[parityPos - 1] = count % 2; /* even parity */
    }
}

/* ---------------------------------------------------------
   Detects error position and corrects it (if any)
   Returns the error position (0 if no error)
--------------------------------------------------------- */
int detectAndCorrect(int received[], int totalBits, int r) {
    int errorPos = 0;

    for (int i = 0; i < r; i++) {
        int parityPos = (int) pow(2, i);
        int count = 0;

        for (int pos = 1; pos <= totalBits; pos++) {
            if (pos & parityPos) {
                count += received[pos - 1];
            }
        }
        if (count % 2 != 0)
            errorPos += parityPos;
    }

    if (errorPos != 0) {
        printf("\n>> Error detected at position: %d\n", errorPos);
        received[errorPos - 1] = !received[errorPos - 1]; /* flip the bit */
        printf(">> Bit corrected. Corrected code is now valid.\n");
    } else {
        printf("\n>> No error detected. Data is correct.\n");
    }

    return errorPos;
}

/* ---------------------------------------------------------
   Utility: Display an array of bits with a message
--------------------------------------------------------- */
void displayCode(int arr[], int n, const char *msg) {
    printf("%s", msg);
    for (int i = 0; i < n; i++)
        printf("%d", arr[i]);
    printf("\n");
}

/* ---------------------------------------------------------
   MAIN PROGRAM
--------------------------------------------------------- */
int main() {
    int dataBits, r, totalBits;
    int data[50], encoded[100], received[100];

    printf("=================================================\n");
    printf("        HAMMING CODE - ERROR DETECTION & CORRECTION\n");
    printf("=================================================\n\n");

    /* ---------- Input data ---------- */
    printf("Enter number of data bits: ");
    scanf("%d", &dataBits);

    printf("Enter data bits (space separated, 0s and 1s): ");
    for (int i = 0; i < dataBits; i++)
        scanf("%d", &data[i]);

    /* ---------- Calculate redundant bits ---------- */
    r = calculateParityBits(dataBits);
    totalBits = dataBits + r;

    printf("\nNumber of redundant (parity) bits required: %d\n", r);
    printf("Total length of Hamming code: %d\n", totalBits);

    /* ---------- Encode ---------- */
    encodeHamming(data, dataBits, encoded, totalBits, r);
    printf("\n----------- ENCODING -----------\n");
    displayCode(encoded, totalBits, "Generated Hamming Code : ");

    /* Copy encoded code into 'received' to simulate transmission */
    for (int i = 0; i < totalBits; i++)
        received[i] = encoded[i];

    /* ---------- Simulate error ---------- */
    int choice;
    printf("\nDo you want to introduce an error for testing?\n");
    printf("1. Yes   2. No\nEnter choice: ");
    scanf("%d", &choice);

    if (choice == 1) {
        int pos;
        printf("Enter bit position to flip (1 to %d): ", totalBits);
        scanf("%d", &pos);
        if (pos >= 1 && pos <= totalBits) {
            received[pos - 1] = !received[pos - 1];
            printf("Bit at position %d flipped (error introduced).\n", pos);
        } else {
            printf("Invalid position. No error introduced.\n");
        }
    }

    printf("\n----------- TRANSMISSION -----------\n");
    displayCode(received, totalBits, "Received Code (at receiver): ");

    /* ---------- Detect & Correct ---------- */
    printf("\n----------- DECODING -----------\n");
    detectAndCorrect(received, totalBits, r);

    displayCode(received, totalBits, "Final Corrected Code       : ");

    /* ---------- Extract original data bits ---------- */
    printf("\n----------- EXTRACTED DATA -----------\n");
    printf("Recovered Data Bits        : ");
    for (int i = 1; i <= totalBits; i++) {
        if (!isPowerOfTwo(i))
            printf("%d", received[i - 1]);
    }
    printf("\n\n=================================================\n");

    return 0;
}
