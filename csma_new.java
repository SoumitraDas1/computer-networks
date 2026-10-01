import java.util.Random;
import java.util.Scanner;

public class CSMA {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Random rand = new Random();

        System.out.print("Enter number of stations: ");
        int n = sc.nextInt();

        boolean channelBusy = false;

        for (int i = 1; i <= n; i++) {
            System.out.println("\nStation " + i + " is sensing the channel...");

            if (!channelBusy) {
                System.out.println("Channel is free.");

                if (rand.nextBoolean()) {
                    System.out.println("Station " + i + " is transmitting data.");
                    channelBusy = true;
                } else {
                    System.out.println("Station " + i + " is waiting.");
                }
            } else {
                System.out.println("Channel is busy. Station " + i + " waits.");
            }

            // Simulate transmission completion
            if (channelBusy) {
                System.out.println("Transmission completed.");
                channelBusy = false;
            }
        }

        sc.close();
    }
}
