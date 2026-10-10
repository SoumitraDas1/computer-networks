#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define MAX_STATIONS 10
#define MAX_ATTEMPTS 5
typedef struct {
    int id;
    int arrivalTime;  
    int attempt;     
    int transmitted;     
    int transmitTime;    
} Station;
int getBackoffTime(int attempt) {
    int limit = 1;
    for (int i = 0; i < attempt && i < MAX_ATTEMPTS; i++)
        limit *= 2;              // limit = 2^attempt
    return rand() % limit;       // random value in [0, 2^attempt - 1]
}
int main() {
    int n, propagationDelay, transmissionTime;
    Station stations[MAX_STATIONS];
    srand(time(NULL));
    printf("=== CSMA/CD Simulation ===\n\n");
    printf("Enter number of stations: ");
    scanf("%d", &n);
    printf("Enter transmission time (slots) for a frame: ");
    scanf("%d", &transmissionTime);
    printf("Enter propagation delay (slots): ");
    scanf("%d", &propagationDelay);
    for (int i = 0; i < n; i++) {
        stations[i].id = i + 1;
        stations[i].arrivalTime = rand() % 10;
        stations[i].attempt = 0;
        stations[i].transmitted = 0;
        stations[i].transmitTime = stations[i].arrivalTime;
        printf("Station %d ready to send at time slot: %d\n",
               stations[i].id, stations[i].arrivalTime);
    }
    printf("\n--- Starting Simulation ---\n");
    int remaining = n;
    int currentTime = 0;
    int maxSimTime = 100;
    while (remaining > 0 && currentTime < maxSimTime) {
        int contenders[MAX_STATIONS];
        int count = 0;
        for (int i = 0; i < n; i++) {
            if (!stations[i].transmitted &&
                stations[i].transmitTime == currentTime) {
                contenders[count++] = i;
            }
        }
        if (count == 1) {
            int idx = contenders[0];
            stations[idx].transmitted = 1;
            remaining--;
            printf("Time %d: Station %d transmits SUCCESSFULLY (frame takes %d slots)\n",
                   currentTime, stations[idx].id, transmissionTime);
        }
        else if (count > 1) {
            printf("Time %d: COLLISION detected among stations: ", currentTime);
            for (int j = 0; j < count; j++)
                printf("%d ", stations[contenders[j]].id);
            printf("\n");
            for (int j = 0; j < count; j++) {
                int idx = contenders[j];
                stations[idx].attempt++;
                if (stations[idx].attempt > MAX_ATTEMPTS) {
                    printf("  Station %d: transmission FAILED (max attempts reached)\n",
                           stations[idx].id);
                    stations[idx].transmitted = 1;
                    remaining--;
                    continue;
                }
                int backoff = getBackoffTime(stations[idx].attempt);
                stations[idx].transmitTime = currentTime + backoff + propagationDelay + 1;
                printf("  Station %d: backing off, will retry at time slot %d (attempt %d)\n",
                       stations[idx].id, stations[idx].transmitTime, stations[idx].attempt);
            }
        }
        currentTime++;
    }
    printf("\n--- Simulation Summary ---\n");
    for (int i = 0; i < n; i++) {
        if (stations[i].transmitted && stations[i].attempt <= MAX_ATTEMPTS)
            printf("Station %d: Transmitted successfully (Attempts: %d)\n",
                   stations[i].id, stations[i].attempt + 1);
        else
            printf("Station %d: Transmission FAILED after max attempts\n",
                   stations[i].id);
    }
    if (currentTime >= maxSimTime)
        printf("\nNote: Simulation stopped at time limit (%d slots).\n", maxSimTime);
    return 0;
}
