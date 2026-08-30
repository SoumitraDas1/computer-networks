#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_FRAMES 20

int main()
{
    int n, i;
    int transmitted[MAX_FRAMES] = {0};
    int success = 0, collisions = 0;
    int active;

    srand(time(0));

    printf("Enter number of frames: ");
    scanf("%d", &n);

    printf("\n--- Pure ALOHA Simulation ---\n");

    active = n;

    while (active > 0)
    {
        int count = 0;
        int last = -1;

        /* Randomly decide which frames transmit */
        for (i = 0; i < n; i++)
        {
            if (!transmitted[i])
            {
                if (rand() % 2 == 0)
                {
                    count++;
                    last = i;
                }
            }
        }

        if (count == 0)
        {
            printf("No frame transmitted in this slot.\n");
        }
        else if (count == 1)
        {
            printf("Frame %d transmitted successfully.\n", last + 1);
            transmitted[last] = 1;
            success++;
            active--;
        }
        else
        {
            printf("Collision occurred between %d frames.\n", count);
            collisions++;
            printf("Frames will retransmit after random backoff.\n");
        }
    }

    printf("\n--- Simulation Result ---\n");
    printf("Total Frames       : %d\n", n);
    printf("Successful Frames  : %d\n", success);
    printf("Total Collisions   : %d\n", collisions);

    return 0;
}