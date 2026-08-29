"""
Pure ALOHA Network Simulation

This program simulates the Pure ALOHA protocol and compares
the simulated throughput with the theoretical throughput.
"""
#Name : Biswajit Bagdi
#Roll : 21

import math
import random
import matplotlib.pyplot as plt

# -----------------------------
# Simulation Parameters
# -----------------------------

SIMULATION_TIME = 1000  # Total simulation duration (seconds)
PACKET_DURATION = 1.0  # Packet transmission time (seconds)
NUM_STATIONS = 20  # Number of transmitting stations
RANDOM_SEED = 42  # Set seed for reproducible results

OFFERED_LOADS = [
    0.1, 0.2, 0.3, 0.4, 0.5,
    0.6, 0.7, 0.8, 0.9, 1.0,
    1.2, 1.4, 1.6, 1.8, 2.0
]


def generate_packets(load: float) -> list[dict]:
    """Generate transmission events for all stations based on offered load."""
    packets = []

    for station in range(NUM_STATIONS):
        current_time = random.expovariate(load / NUM_STATIONS)

        while current_time < SIMULATION_TIME:
            packets.append({
                "station": station,
                "start": current_time,
                "end": current_time + PACKET_DURATION,
                "success": True
            })
            current_time += random.expovariate(load / NUM_STATIONS)

    packets.sort(key=lambda packet: packet["start"])
    return packets


def detect_collisions(packets: list[dict]) -> None:
    """Detect overlapping packet transmissions and mark collisions."""
    total_packets = len(packets)

    for i in range(total_packets):
        for j in range(i + 1, total_packets):
            if packets[j]["start"] >= packets[i]["end"]:
                break

            packets[i]["success"] = False
            packets[j]["success"] = False


def simulate_pure_aloha():
    """Run the Pure ALOHA simulation for different offered loads."""
    random.seed(RANDOM_SEED)
    simulated_throughput = []
    theoretical_throughput = []

    print("\n========== Pure ALOHA Simulation ==========\n")

    for load in OFFERED_LOADS:
        packets = generate_packets(load)
        detect_collisions(packets)

        total_generated = len(packets)
        successful_packets = sum(packet["success"] for packet in packets)
        collided_packets = total_generated - successful_packets
        collision_rate = (collided_packets / total_generated * 100) if total_generated > 0 else 0.0

        throughput = (successful_packets * PACKET_DURATION) / SIMULATION_TIME
        simulated_throughput.append(throughput)

        theo_val = load * math.exp(-2 * load)
        theoretical_throughput.append(theo_val)

        print(f"Offered Load (G)       : {load:.2f}")
        print(f"Generated Packets      : {total_generated}")
        print(f"Successful Packets     : {successful_packets}")
        print(f"Collided Packets       : {collided_packets} ({collision_rate:.1f}%)")
        print(f"Simulated Throughput   : {throughput:.4f} (Theoretical: {theo_val:.4f})")
        print("-" * 45)

    return simulated_throughput, theoretical_throughput


def plot_results(simulated, theoretical):
    """Plot simulated and theoretical throughput with peak marker."""
    plt.figure(figsize=(9, 5))

    plt.plot(
        OFFERED_LOADS,
        simulated,
        "bo-",
        linewidth=2,
        markersize=6,
        label="Simulation"
    )

    plt.plot(
        OFFERED_LOADS,
        theoretical,
        "r--",
        linewidth=2,
        label=r"Theoretical ($S = G e^{-2G}$)"
    )

    # Highlight theoretical maximum throughput (G = 0.5, S ≈ 0.1839)
    max_g = 0.5
    max_s = max_g * math.exp(-2 * max_g)
    plt.plot(max_g, max_s, "go", markersize=8, label=f"Max Theoretical S ({max_s:.3f})")

    plt.title("Pure ALOHA Throughput Analysis")
    plt.xlabel("Offered Load (G)")
    plt.ylabel("Throughput (S)")

    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    """Program entry point."""
    simulated, theoretical = simulate_pure_aloha()
    plot_results(simulated, theoretical)


if __name__ == "__main__":
    main()
