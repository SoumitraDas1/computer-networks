import java.util.Scanner;

public class HammingCode {

    static int[] encode(int[] data) {
        int[] h = new int[8]; // positions 1 to 7


        h[3] = data[0];
        h[5] = data[1];
        h[6] = data[2];
        h[7] = data[3];

        // Calculate parity bits
        h[1] = h[3] ^ h[5] ^ h[7]; // P1
        h[2] = h[3] ^ h[6] ^ h[7]; // P2
        h[4] = h[5] ^ h[6] ^ h[7]; // P4

        return h;
    }

    static void detectAndCorrect(int[] h) {

        int p1 = h[1] ^ h[3] ^ h[5] ^ h[7];
        int p2 = h[2] ^ h[3] ^ h[6] ^ h[7];
        int p4 = h[4] ^ h[5] ^ h[6] ^ h[7];

        int errorPosition = p4 * 4 + p2 * 2 + p1;

        if (errorPosition == 0) {
            System.out.println("No error detected.");
        } else {
            System.out.println("Error detected at position: " + errorPosition);

            h[errorPosition] ^= 1;

            System.out.println("Error corrected.");
        }
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int[] data = new int[4];

        System.out.print("Enter 4 data bits: ");

        for (int i = 0; i < 4; i++) {
            data[i] = sc.nextInt();
        }

        int[] hamming = encode(data);

        System.out.print("Generated Hamming Code: ");

        for (int i = 1; i <= 7; i++) {
            System.out.print(hamming[i]);
        }

        System.out.print("\nEnter error position (0 for no error): ");
        int error = sc.nextInt();

        if (error >= 1 && error <= 7) {
            hamming[error] ^= 1;
        }

        System.out.print("Received Hamming Code: ");

        for (int i = 1; i <= 7; i++) {
            System.out.print(hamming[i]);
        }

        System.out.println();

        // Detect and correct
        detectAndCorrect(hamming);

        System.out.print("Corrected Hamming Code: ");

        for (int i = 1; i <= 7; i++) {
            System.out.print(hamming[i]);
        }

        System.out.println();

        sc.close();
    }
}
