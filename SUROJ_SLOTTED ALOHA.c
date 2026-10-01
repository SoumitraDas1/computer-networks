#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define MAX_STATIONS 50
#define MAX_SLOTS    1000
typedef struct {
    int id;             // Station ID
    int hasPacket;      // 1 if station currently has a packet to send
    int transmitting;   // 1 if station attempts transmission this slot
    int packetsSent;    // total packets successfully sent
    int attempts;        // total transmission attempts
} Station;
/* Function Prototypes */
void initStations(Station stations[], int n);
int  generateTraffic(Station stations[], int n, double arrivalProb);
int  runSlot(Station stations[], int n, double transmitProb, int slotNum, int verbose);
void printSummary(Station stations[], int n, int totalSlots, int successSlots,
                   int collisionSlots, int idleSlots);
int main(void) {
    int numStations;
    int numSlots;
    double arrivalProb;   // probability a station generates a new packet in a slot
    double transmitProb;  // probability a station with a packet transmits in a slot
    int verbose;
    srand((unsigned int) time(NULL));
    printf("===============================================\n");
    printf("      SLOTTED ALOHA NETWORK SIMULATION\n");
    printf("===============================================\n\n");
    /* ---- User Input ---- */
    printf("Enter number of stations (1-%d): ", MAX_STATIONS);
    if (scanf("%d", &numStations) != 1 || numStations < 1 || numStations > MAX_STATIONS) {
        printf("Invalid number of stations. Exiting.\n");
        return 1;
    }
    printf("Enter number of time slots to simulate (1-%d): ", MAX_SLOTS);
    if (scanf("%d", &numSlots) != 1 || numSlots < 1 || numSlots > MAX_SLOTS) {
        printf("Invalid number of slots. Exiting.\n");
        return 1;
    }
    printf("Enter packet arrival probability per station (0.0 - 1.0): ");
    if (scanf("%lf", &arrivalProb) != 1 || arrivalProb < 0.0 || arrivalProb > 1.0) {
        printf("Invalid probability. Exiting.\n");
        return 1;
    }
    printf("Enter transmission probability p (0.0 - 1.0): ");
    if (scanf("%lf", &transmitProb) != 1 || transmitProb < 0.0 || transmitProb > 1.0) {
        printf("Invalid probability. Exiting.\n");
        return 1;
    }
    printf("Show slot-by-slot details? (1 = Yes, 0 = No): ");
    if (scanf("%d", &verbose) != 1) verbose = 0;
    /* ---- Setup ---- */
    Station stations[MAX_STATIONS];
    initStations(stations, numStations);
    int successSlots = 0;
    int collisionSlots = 0;
    int idleSlots = 0;
    printf("\nStarting simulation...\n\n");
    if (verbose) {
        printf("%-6s %-10s %-25s\n", "Slot", "Result", "Details");
        printf("---------------------------------------------\n");
    }
    /* ---- Main Simulation Loop ---- */
    for (int slot = 1; slot <= numSlots; slot++) {
        /* New packets may arrive for stations that are currently idle */
        generateTraffic(stations, numStations, arrivalProb);
        /* Run one slot: stations with packets attempt transmission with transmitProb */
        int result = runSlot(stations, numStations, transmitProb, slot, verbose);

        if (result == 1)      successSlots++;
        else if (result == 2) collisionSlots++;
        else                  idleSlots++;
    }
    /* ---- Results ---- */
    printSummary(stations, numStations, numSlots, successSlots, collisionSlots, idleSlots);
    return 0;
}
/* Initialize all stations to have no packet and zero counters */
void initStations(Station stations[], int n) {
    for (int i = 0; i < n; i++) {
        stations[i].id = i + 1;
        stations[i].hasPacket = 0;
        stations[i].transmitting = 0;
        stations[i].packetsSent = 0;
        stations[i].attempts = 0;
    }
}
/* Each idle station may generate a new packet with probability arrivalProb */
int generateTraffic(Station stations[], int n, double arrivalProb) {
    int newPackets = 0;
    for (int i = 0; i < n; i++) {
        if (!stations[i].hasPacket) {
            double r = (double) rand() / RAND_MAX;
            if (r < arrivalProb) {
                stations[i].hasPacket = 1;
                newPackets++;
            }
        }
    }
    return newPackets;
}
int runSlot(Station stations[], int n, double transmitProb, int slotNum, int verbose) {
    int transmittersCount = 0;
    int transmitterIndex = -1;

    for (int i = 0; i < n; i++) {
        stations[i].transmitting = 0;
        if (stations[i].hasPacket) {
            double r = (double) rand() / RAND_MAX;
            if (r < transmitProb) {
                stations[i].transmitting = 1;
                stations[i].attempts++;
                transmittersCount++;
                transmitterIndex = i;
            }
        }
    }

    if (transmittersCount == 0) {
        if (verbose)
            printf("%-6d %-10s %-25s\n", slotNum, "IDLE", "No station transmitted");
        return 0;
    } else if (transmittersCount == 1) {
        stations[transmitterIndex].hasPacket = 0;
        stations[transmitterIndex].packetsSent++;
        if (verbose) {
            char detail[40];
            sprintf(detail, "Station %d transmitted", stations[transmitterIndex].id);
            printf("%-6d %-10s %-25s\n", slotNum, "SUCCESS", detail);
        }
        return 1;
    } else {
        if (verbose) {
            char detail[60];
            sprintf(detail, "%d stations collided", transmittersCount);
            printf("%-6d %-10s %-25s\n", slotNum, "COLLISION", detail);
        }
        return 2;
    }
}
/* Print final statistics: throughput, efficiency, per-station stats */
void printSummary(Station stations[], int n, int totalSlots, int successSlots,
                   int collisionSlots, int idleSlots) {
    printf("\n===============================================\n");
    printf("              SIMULATION SUMMARY\n");
    printf("===============================================\n");
    printf("Total slots simulated : %d\n", totalSlots);
    printf("Successful slots       : %d\n", successSlots);
    printf("Collision slots        : %d\n", collisionSlots);
    printf("Idle slots              : %d\n", idleSlots);
    double throughput = (double) successSlots / totalSlots;
    printf("\nThroughput (S)          : %.4f packets/slot\n", throughput);
    printf("Efficiency              : %.2f%%\n", throughput * 100.0);
    printf("\n--- Per-Station Statistics ---\n");
    printf("%-10s %-15s %-15s\n", "Station", "Attempts", "PacketsSent");
    int totalAttempts = 0, totalSent = 0;
    for (int i = 0; i < n; i++) {
        printf("%-10d %-15d %-15d\n", stations[i].id, stations[i].attempts,
               stations[i].packetsSent);
        totalAttempts += stations[i].attempts;
        totalSent += stations[i].packetsSent;
    }
    printf("---------------------------------------------\n");
    printf("Total attempts          : %d\n", totalAttempts);
    printf("Total packets delivered : %d\n", totalSent);
    if (totalAttempts > 0)
        printf("Success rate per attempt : %.2f%%\n",
               (double) totalSent / totalAttempts * 100.0);
    printf("===============================================\n");
    printf(" Theoretical max throughput for Slotted ALOHA\n");
    printf(" is S_max = 1/e ≈ 0.368 (36.8%%) at G = 1\n");
    printf("===============================================\n");
}
