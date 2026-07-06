import random
import time

# -----------------------------
# CSMA Protocol Simulation
# -----------------------------

class Station:
    def __init__(self, station_id):
        self.id = station_id
        self.backoff = 0

class CSMASimulator:

    def __init__(self, num_stations, num_slots):
        self.num_stations = num_stations
        self.num_slots = num_slots
        self.stations = [Station(i + 1) for i in range(num_stations)]

    # ---------------- CSMA/CD ----------------
    def simulate_cd(self):

        print("\n==============================")
        print("      CSMA/CD SIMULATION")
        print("==============================")

        for slot in range(1, self.num_slots + 1):

            print(f"\nTime Slot : {slot}")

            transmitting = []

            # Check which stations are ready
            for station in self.stations:

                if station.backoff > 0:
                    station.backoff -= 1
                    continue

                if random.random() < 0.5:
                    transmitting.append(station)

            if len(transmitting) == 0:
                print("Channel Status : Idle")

            elif len(transmitting) == 1:
                print(f"Station {transmitting[0].id} transmitted successfully.")

            else:
                print("Collision Detected!")

                print("Stations Involved : ", end="")
                for s in transmitting:
                    print(s.id, end=" ")

                print()

                for s in transmitting:
                    s.backoff = random.randint(1, 5)
                    print(f"Station {s.id} waits {s.backoff} slots.")

            print("\nCurrent Backoff Values")

            for s in self.stations:
                print(f"Station {s.id} : {s.backoff}")

            time.sleep(1)

        print("\nCSMA/CD Simulation Completed.")

    # ---------------- CSMA/CA ----------------
    def simulate_ca(self):

        print("\n==============================")
        print("      CSMA/CA SIMULATION")
        print("==============================")

        for slot in range(1, self.num_slots + 1):

            print(f"\nTime Slot : {slot}")

            ready = []

            for station in self.stations:

                if station.backoff > 0:
                    station.backoff -= 1
                    continue

                if random.random() < 0.5:
                    ready.append(station)

            if len(ready) == 0:

                print("Channel Idle")

            elif len(ready) == 1:

                s = ready[0]

                print(f"Station {s.id} senses idle channel.")
                print("RTS Sent")
                print("CTS Received")
                print("DATA Transmitted")
                print("ACK Received")

                s.backoff = random.randint(1, 4)

            else:

                print("Multiple Stations Ready")

                for s in ready:
                    print("Station", s.id)

                winner = random.choice(ready)

                print(f"\nStation {winner.id} wins the channel.")

                print("RTS -> CTS -> DATA -> ACK")

                winner.backoff = random.randint(1, 4)

                for s in ready:
                    if s != winner:
                        s.backoff = random.randint(2, 6)

            print("\nCurrent Backoff Values")

            for s in self.stations:
                print(f"Station {s.id} : {s.backoff}")

            time.sleep(1)

        print("\nCSMA/CA Simulation Completed.")


# ---------------- MAIN PROGRAM ----------------

print("===================================")
print("      CSMA PROTOCOL SIMULATOR")
print("===================================")

stations = int(input("Enter Number of Stations : "))
slots = int(input("Enter Number of Time Slots : "))

simulator = CSMASimulator(stations, slots)

while True:

    print("\n========== MENU ==========")
    print("1. Simulate CSMA/CD")
    print("2. Simulate CSMA/CA")
    print("3. Exit")

    choice = input("Enter Your Choice : ")

    if choice == "1":
        simulator.simulate_cd()

    elif choice == "2":
        simulator.simulate_ca()

    elif choice == "3":
        print("\nThank You!")
        print("Program Terminated Successfully.")
        break

    else:
        print("Invalid Choice! Try Again.")