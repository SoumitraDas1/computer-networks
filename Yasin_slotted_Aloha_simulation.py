"""
Simulation of the Slotted ALOHA protocol.

This program simulates Slotted ALOHA for different contention window
sizes and evaluates the slot efficiency as the number of nodes increases.
"""

import random
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Simulation Parameters
# ---------------------------------------------------------------------

TOTAL_SLOTS = 100_000
MAX_NODES = 32
WINDOW_SIZES = (8, 16, 32)
RANDOM_SEED = 42

# Fixed seed for reproducible results
random.seed(RANDOM_SEED)


class Node:
    """
    Represents a node participating in the Slotted ALOHA protocol.
    Each node maintains a random backoff timer.
    """

    def __init__(self, window_size: int) -> None:
        self.window_size = window_size
        self.timer = random.randint(0, window_size - 1)

    def tick(self) -> None:
        """
        Decrease the backoff timer by one time slot.
        """
        if self.timer > 0:
            self.timer -= 1

    def reset_backoff(self) -> None:
        """
        Assign a new random backoff timer after a
        successful transmission or a collision.
        """
        self.timer = random.randint(0, self.window_size - 1)


def simulate(window_size: int, max_nodes: int) -> tuple[list[int], list[float]]:
    """
    Simulate the Slotted ALOHA protocol.

    Parameters
    ----------
    window_size : int
        Contention window size.
    max_nodes : int
        Maximum number of nodes to simulate.

    Returns
    -------
    tuple[list[int], list[float]]
        Lists containing the number of nodes and their corresponding
        slot efficiencies.
    """

    node_counts = []
    efficiencies = []

    print(f"\n{'=' * 55}")
    print(f"Simulation for Contention Window = {window_size}")
    print(f"{'=' * 55}")

    for node_count in range(1, max_nodes + 1):

        nodes = [Node(window_size) for _ in range(node_count)]
        successful_transmissions = 0

        for _ in range(TOTAL_SLOTS):

            ready_nodes = []

            for index, node in enumerate(nodes):
                if node.timer == 0:
                    ready_nodes.append(index)
                else:
                    node.tick()

            # Successful transmission
            if len(ready_nodes) == 1:
                successful_transmissions += 1
                nodes[ready_nodes[0]].reset_backoff()

            # Collision
            elif len(ready_nodes) > 1:
                for index in ready_nodes:
                    nodes[index].reset_backoff()

        efficiency = successful_transmissions / TOTAL_SLOTS

        print(
            f"Nodes: {node_count:2d} | "
            f"Successful Slots: {successful_transmissions:6d} | "
            f"Efficiency: {efficiency:.4f}"
        )

        node_counts.append(node_count)
        efficiencies.append(efficiency)

    return node_counts, efficiencies


def plot_results() -> None:
    """
    Run the simulation for each contention window
    and display the efficiency graph.
    """

    plt.figure(figsize=(9, 6))

    for window_size in WINDOW_SIZES:
        nodes, efficiencies = simulate(window_size, MAX_NODES)

        plt.plot(
            nodes,
            efficiencies,
            marker="o",
            linewidth=2,
            markersize=5,
            label=f"Window = {window_size}",
        )

    plt.title("Simulation of Slotted ALOHA", fontsize=14)
    plt.xlabel("Number of Nodes", fontsize=12)
    plt.ylabel("Slot Efficiency", fontsize=12)

    plt.xticks(range(1, MAX_NODES + 1, 2))
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(title="Contention Window")

    plt.tight_layout()
    plt.show()


def main() -> None:
    """Program entry point."""
    plot_results()


if __name__ == "__main__":
    main()