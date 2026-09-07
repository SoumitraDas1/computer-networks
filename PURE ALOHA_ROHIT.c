#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define MAX_STATIONS 20
int main() {
    int n, i, j;
    float arrival[MAX_STATIONS], transmission_time[MAX_STATIONS];
    float start[MAX_STATIONS], end[MAX_STATIONS];
    int collision[MAX_STATIONS] = {0};
    int total_collisions = 0;
    printf("=== PURE ALOHA PROTOCOL SIMULATION ===\n\n");
    printf("Enter number of stations: ");
    scanf("%d", &n);
    if (n > MAX_STATIONS) {
        printf("Too many stations. Max allowed: %d\n", MAX_STATIONS);
        return 1;
    }
    for (i = 0; i < n; i++) {
        printf("\nStation %d:\n", i + 1);
        printf("  Enter arrival time: ");
        scanf("%f", &arrival[i]);
        printf("  Enter transmission time: ");
        scanf("%f", &transmission_time[i]);
        start[i] = arrival[i];
        end[i] = start[i] + transmission_time[i];
    }
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            if (i != j) {
                if (start[i] < end[j] && start[j] < end[i]) {
                    collision[i] = 1;
                }
            }
        }
    }
    printf("\n%-10s %-10s %-15s %-10s %-10s %-10s\n",
           "Station", "Arrival", "Trans.Time", "Start", "End", "Status");
    printf("---------------------------------------------------------------\n");
    for (i = 0; i < n; i++) {
        printf("%-10d %-10.2f %-15.2f %-10.2f %-10.2f %-10s\n",
               i + 1, arrival[i], transmission_time[i],
               start[i], end[i],
               collision[i] ? "COLLISION" : "SUCCESS");
        if (collision[i])
            total_collisions++;
    }
    printf("\nTotal Successful Transmissions: %d\n", n - total_collisions);
    printf("Total Collisions: %d\n", total_collisions);
    float efficiency = ((float)(n - total_collisions) / n) * 100;
    printf("Throughput Efficiency: %.2f%%\n", efficiency);
    return 0;
}
