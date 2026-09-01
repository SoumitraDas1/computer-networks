import java.util.Scanner;

public class HammingCode {

    // Calculate number of redundancy (parity) bits required
    public static int calculateParityBits(int m) {
        int r = 0;
        while (Math.pow(2, r) < (m + r + 1)) {
            r++;
        }
        return r;
    }

    // Encode data bits into Hamming code
    public static int[] encode(int[] data) {
        int m = data.length;
        int r = calculateParityBits(m);
        int n = m + r;
        int[] encoded = new int[n];

        // Place data bits into non-power-of-2 positions
        int j = 0;
        for (int i = 1; i <= n; i++) {
            if ((i & (i - 1)) != 0) { // not a power of 2
                encoded[i - 1] = data[j++];
            }
        }

        // Calculate and set parity bits
        for (int i = 0; i < r; i++) {
            int position = (int) Math.pow(2, i);
            int parity = 0;
            for (int k = position; k <= n; k++) {
                if ((k & position) != 0) {
                    parity ^= encoded[k - 1];
                }
            }
            encoded[position - 1] = parity;
        }

        return encoded;
    }

    // Detect and correct single-bit error; returns corrected code
    public static int[] decode(int[] received) {
        int n = received.length;
        int r = 0;
        while (Math.pow(2, r) < n + 1) r++;

        int errorPosition = 0;

        for (int i = 0; i < r; i++) {
            int position = (int) Math.pow(2, i);
            int parity = 0;
            for (int k = position; k <= n; k++) {
                if ((k & position) != 0) {
                    parity ^= received[k - 1];
                }
            }
            if (parity != 0) {
                errorPosition += position;
            }
        }

        int[] corrected = received.clone();

        if (errorPosition == 0) {
            System.out.println("No error detected.");
        } else if (errorPosition > n) {
            System.out.println("Error detected at invalid position: " + errorPosition
                    + " (possible multi-bit error, cannot correct).");
        } else {
            System.out.println("Error detected at position: " + errorPosition + " — correcting...");
            corrected[errorPosition - 1] ^= 1; // flip the erroneous bit
        }

        return corrected;
    }

    // Extract original data bits from a corrected Hamming code
    public static int[] extractData(int[] corrected) {
        int n = corrected.length;
        int r = 0;
        while (Math.pow(2, r) < n + 1) r++;

        int m = n - r;
        int[] data = new int[m];
        int j = 0;

        for (int i = 1; i <= n; i++) {
            if ((i & (i - 1)) != 0) { // not a power of 2 -> data bit
                data[j++] = corrected[i - 1];
            }
        }
        return data;
    }

    public static void printArray(String label, int[] arr) {
        System.out.print(label + ": ");
        for (int bit : arr) System.out.print(bit);
        System.out.println();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of data bits: ");
        int m = Integer.parseInt(sc.nextLine().trim());

        int[] data = new int[m];
        System.out.println("Enter " + m + " data bits (0 or 1), one at a time:");
        for (int i = 0; i < m; i++) {
            data[i] = Integer.parseInt(sc.nextLine().trim());
        }

        // Encoding
        int[] encoded = encode(data);
        printArray("Original Data", data);
        printArray("Encoded Hamming Code", encoded);

        // Simulate transmission — let user introduce an error (optional)
        System.out.print("Enter bit position to flip (simulate error), or 0 for no error: ");
        int flipPos = Integer.parseInt(sc.nextLine().trim());

        int[] transmitted = encoded.clone();
        if (flipPos >= 1 && flipPos <= transmitted.length) {
            transmitted[flipPos - 1] ^= 1;
            System.out.println("Bit at position " + flipPos + " flipped to simulate transmission error.");
        }
        printArray("Transmitted (possibly corrupted) Code", transmitted);

        // Decoding: detect & correct
        int[] corrected = decode(transmitted);
        printArray("Corrected Code", corrected);

        // Extract original data
        int[] extractedData = extractData(corrected);
        printArray("Extracted Data", extractedData);

        sc.close();
    }
}
