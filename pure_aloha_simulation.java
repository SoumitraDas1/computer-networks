import java.util.Random;
import java.util.Scanner;

public class pure_aloha_simulation {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        Random random = new Random();

        System.out.print("Enter number of stations: ");
        int stations = sc.nextInt();

        System.out.print("Enter number of time slots: ");
        int slots = sc.nextInt();

        int successful = 0;
        int collision = 0;
        int idle = 0;

        for (int i = 1; i <= slots; i++) {

            int transmission = 0;

            // Each station may transmit randomly
            for (int j = 1; j <= stations; j++) {
                if (random.nextBoolean()) {
                    transmission++;
                }
            }

            System.out.print("Time Slot " + i + ": ");

            if (transmission == 0) {
                System.out.println("Channel is IDLE");
                idle++;
            }
            else if (transmission == 1) {
                System.out.println("Successful Transmission");
                successful++;
            }
            else {
                System.out.println("COLLISION");
                collision++;
            }
        }

        double throughput = (double) successful / slots;

        System.out.println("\n----- PURE ALOHA RESULTS -----");
        System.out.println("Total Slots       : " + slots);
        System.out.println("Successful        : " + successful);
        System.out.println("Collisions        : " + collision);
        System.out.println("Idle Slots        : " + idle);
        System.out.printf("Throughput        : %.2f%n", throughput);

        sc.close();
    }
}
