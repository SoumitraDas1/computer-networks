"""
Dijkstra's Shortest Path Algorithm

Author: Deepsikha Das

Description:
This program calculates the shortest path and minimum path cost
from a source router to every other router in a weighted
computer network.

The graph is represented using an adjacency list.
A min-heap (priority queue) is used to efficiently find
the shortest paths.

Important:
Dijkstra's algorithm requires all edge weights to be non-negative.
"""


import heapq
from typing import List, Tuple


# Represents an edge as:
# (destination_router, edge_weight)
Edge = Tuple[int, int]


def add_link(
    graph: List[List[Edge]],
    source: int,
    destination: int,
    cost: int
) -> None:
    """
    Add a bidirectional link between two routers.

    Args:
        graph: Network graph represented as an adjacency list.
        source: Source router number.
        destination: Destination router number.
        cost: Cost of the network link.
    """
    if cost < 0:
        raise ValueError(
            "Dijkstra's algorithm requires non-negative edge weights."
        )

    graph[source].append((destination, cost))
    graph[destination].append((source, cost))


def reconstruct_path(
    destination: int,
    parent: List[int]
) -> List[int]:
    """
    Reconstruct the shortest path from the source router
    to the destination router.

    Args:
        destination: Destination router.
        parent: Parent router for each router.

    Returns:
        List containing the routers in the shortest path.
    """
    path: List[int] = []
    current = destination

    while current != -1:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def dijkstra(
    source: int,
    graph: List[List[Edge]]
) -> Tuple[List[float], List[int]]:
    """
    Calculate shortest distances from the source router
    to every other router.

    Args:
        source: Starting router.
        graph: Network graph represented as an adjacency list.

    Returns:
        distance: Shortest distance from source to every router.
        parent: Parent router used to reconstruct shortest paths.
    """
    number_of_routers = len(graph)
    infinity = float("inf")

    # Initialize all distances to infinity.
    distance: List[float] = [infinity] * number_of_routers

    # Parent array is used for shortest-path reconstruction.
    parent: List[int] = [-1] * number_of_routers

    # Min-heap containing:
    # (current_shortest_distance, router)
    priority_queue: List[Tuple[float, int]] = []

    # Distance from the source router to itself is zero.
    distance[source] = 0

    heapq.heappush(priority_queue, (0, source))

    while priority_queue:
        current_distance, current_router = heapq.heappop(
            priority_queue
        )

        # Ignore outdated entries in the priority queue.
        if current_distance != distance[current_router]:
            continue

        # Examine all neighbouring routers.
        for next_router, edge_weight in graph[current_router]:

            # Dijkstra's algorithm requires non-negative weights.
            if edge_weight < 0:
                raise ValueError(
                    "Negative edge weight found. "
                    "Dijkstra's algorithm cannot be used."
                )

            # Relaxation step.
            new_distance = current_distance + edge_weight

            if new_distance < distance[next_router]:
                distance[next_router] = new_distance
                parent[next_router] = current_router

                heapq.heappush(
                    priority_queue,
                    (new_distance, next_router)
                )

    return distance, parent


def print_routing_table(
    source: int,
    distance: List[float],
    parent: List[int]
) -> None:
    """
    Display the shortest-path routing table.
    """
    infinity = float("inf")

    print()
    print("=" * 68)
    print("              DIJKSTRA SHORTEST PATH ROUTING TABLE")
    print("=" * 68)
    print(f"Source Router: {source}")
    print()
    print(f"{'Router':<12}{'Distance':<15}Path")
    print("-" * 68)

    for router in range(len(distance)):

        if distance[router] == infinity:
            print(f"{router:<12}{'INF':<15}Unreachable")
            continue

        path = reconstruct_path(router, parent)
        path_string = " -> ".join(str(node) for node in path)

        print(
            f"{router:<12}"
            f"{int(distance[router]):<15}"
            f"{path_string}"
        )

    print("-" * 68)


def main() -> None:
    """
    Build the sample network, run Dijkstra's algorithm,
    and display the resulting routing table.
    """

    # Total number of routers in the network.
    number_of_routers = 6

    # Source router.
    source_router = 0

    # Create an empty adjacency-list graph.
    graph: List[List[Edge]] = [
        [] for _ in range(number_of_routers)
    ]

    # Network topology.
    #
    # Format:
    # add_link(graph, router1, router2, link_cost)

    add_link(graph, 0, 1, 4)
    add_link(graph, 0, 2, 2)
    add_link(graph, 1, 2, 1)
    add_link(graph, 1, 3, 5)
    add_link(graph, 2, 3, 8)
    add_link(graph, 2, 4, 10)
    add_link(graph, 3, 4, 2)
    add_link(graph, 3, 5, 6)
    add_link(graph, 4, 5, 3)

    # Validate the source router.
    if not 0 <= source_router < number_of_routers:
        raise ValueError("Invalid source router.")

    # Run Dijkstra's algorithm.
    distance, parent = dijkstra(
        source_router,
        graph
    )

    # Display the shortest-path routing table.
    print_routing_table(
        source_router,
        distance,
        parent
    )


if __name__ == "__main__":
    main()