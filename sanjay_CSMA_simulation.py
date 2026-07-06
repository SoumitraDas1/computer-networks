import random
import time

class Station:
    def __init__(self, station_id):
        self.station_id = station_id
        self.backoff = 0
        self.success = 0
        self.collision = 0

    def is_ready(self):
        return self.backoff == 0

    def reduce_backoff(self):
        if self.backoff > 0:
            self.backoff -= 1

    def set_backoff(self):
        self.backoff = random.randint(1, 5)


class CSMASimulation:

    def __init__(self, stations, slots):
        self.stations = [Station(i + 1) for i in range(stations)]
        self.slots = slots

    def simulate(self):

        print("\n========== CSMA SIMULATION ==========\n")

        for slot in range(1, self.slots + 1):

            print("=" * 40)
            print("Time Slot :", slot)

            ready = []

            # Check which stations want to transmit
            for station in self.stations:

                if station.backoff > 0:
                    station.reduce_backoff()
                    continue

                want_to_send = random.choice([True, False])

                if want_to_send:
                    ready.append(station)

            # Channel Status
            if len(ready) == 0:

                print("Channel Status : Idle")
                print("No station wants to transmit.")

            elif len(ready) == 1:

                s = ready[0]
                print("Channel Status : Busy")
                print(f"Station {s.station_id} transmitted successfully.")

                s.success += 1

            else:

                print("Collision Occurred!")

                print("Stations involved : ", end="")

                for s in ready:
                    print(s.station_id, end=" ")

                print("\n")

                for s in ready:
                    s.collision += 1
                    s.set_backoff()
                    print(f"Station {s.station_id} backoff = {s.backoff}")

            print("\nBackoff Status")

            for s in self.stations:
                print(f"Station {s.station_id} --> {s.backoff}")

            time.sleep(1)

        # Final Report
        print("\n")
        print("=" * 40)
        print("FINAL REPORT")
        print("=" * 40)

        total_success = 0
        total_collision = 0

        for s in self.stations:

            total_success += s.success
            total_collision += s.collision

            print(f"Station {s.station_id}")
            print(f"Successful Transmissions : {s.success}")
            print(f"Collisions              : {s.collision}")
            print()

        print("----------------------------------------")
        print("Total Successful Transmissions :", total_success)
        print("Total Collisions               :", total_collision)
        print("Simulation Completed Successfully.")


# Main Program

print("===================================")
print("      CSMA SIMULATION PROGRAM")
print("===================================")

stations = int(input("Enter Number of Stations : "))
slots = int(input("Enter Number of Time Slots : "))

simulation = CSMASimulation(stations, slots)
simulation.simulate()