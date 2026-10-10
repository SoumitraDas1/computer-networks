"""
Bellman-Ford shortest-path algorithm for Computer Networks.

Features:
- Supports negative edge weights
- Uses infinity instead of an arbitrary large constant
- Stops early when no distance changes
- Detects reachable negative-weight cycles
- Reconstructs shortest paths when no negative cycle exists
- Validates vertex indices and source vertex
"""

from math import inf
from typing import List, Optional, Tuple


Edge = Tuple[int, int, int]


def bellman_ford(
    graph: List[Edge],
    vertex_count: int,
    source: int
) -> Tuple[List[float], List[Optional[int]], Optional[List[int]]]:
    """
    Run the Bellman-Ford algorithm.

    Returns:
        distance: shortest known distance from source
        predecessor: previous vertex for path reconstruction
        negative_cycle: one reachable negative cycle, if present
    """

    if vertex_count <= 0:
        raise ValueError("Number of vertices must be greater than 0.")

    if not 0 <= source < vertex_count:
        raise ValueError(
            f"Source vertex must be between 0 and {vertex_count - 1}."
        )

    # Validate all edges before processing.
    for u, v, weight in graph:
        if not (0 <= u < vertex_count and 0 <= v < vertex_count):
            raise ValueError(
                f"Invalid edge ({u}, {v}, {weight}). "
                f"Vertices must be between 0 and {vertex_count - 1}."
            )

    distance = [inf] * vertex_count
    predecessor: List[Optional[int]] = [None] * vertex_count

    distance[source] = 0

    # Relax every edge V-1 times.
    for _ in range(vertex_count - 1):
        updated = False

        for u, v, weight in graph:
            if distance[u] != inf and distance[u] + weight < distance[v]:
                distance[v] = distance[u] + weight
                predecessor[v] = u
                updated = True

        # If nothing changed, the algorithm has already converged.
        if not updated:
            break

    # Check for a reachable negative-weight cycle.
    cycle_vertex = None

    for u, v, weight in graph:
        if distance[u] != inf and distance[u] + weight < distance[v]:
            predecessor[v] = u
            cycle_vertex = v
            break

    if cycle_vertex is None:
        return distance, predecessor, None

    # Move backwards V times so that we definitely enter the cycle.
    cycle_start = cycle_vertex

    for _ in range(vertex_count):
        if predecessor[cycle_start] is None:
            return distance, predecessor, None

        cycle_start = predecessor[cycle_start]

    # Reconstruct the cycle.
    cycle = [cycle_start]
    current = predecessor[cycle_start]

    while current is not None and current != cycle_start:
        cycle.append(current)
        current = predecessor[current]

        if len(cycle) > vertex_count:
            break

    cycle.reverse()

    return distance, predecessor, cycle


def build_path(
    predecessor: List[Optional[int]],
    source: int,
    destination: int
) -> List[int]:
    """Build a path from source to destination."""

    path: List[int] = []
    current: Optional[int] = destination

    while current is not None:
        path.append(current)

        if current == source:
            path.reverse()
            return path

        current = predecessor[current]

    return []


def display_results(
    distance: List[float],
    predecessor: List[Optional[int]],
    source: int
) -> None:
    """Display shortest distances and paths."""

    print(f"\nShortest paths from source vertex {source}:")
    print("Vertex\tDistance\tPath")
    print("------\t--------\t----")

    for vertex, cost in enumerate(distance):
        if cost == inf:
            print(f"{vertex}\tINF\t\tNo path")
        else:
            path = build_path(predecessor, source, vertex)
            path_text = " -> ".join(map(str, path))
            print(f"{vertex}\t{int(cost)}\t\t{path_text}")


def main() -> None:
    # Original graph supplied in the question.
    #
    # Important:
    # 1 -> 2 -> 3 -> 1
    # has total weight (-3) + 4 + (-2) = -1.
    #
    # Therefore, this graph contains a reachable negative-weight cycle.

    graph: List[Edge] = [
        (0, 1, 4),
        (0, 2, 5),
        (1, 2, -3),
        (2, 3, 4),
        (3, 1, -2)
    ]

    vertex_count = 4
    source = 0

    distance, predecessor, negative_cycle = bellman_ford(
        graph,
        vertex_count,
        source
    )

    if negative_cycle:
        cycle_text = " -> ".join(
            map(str, negative_cycle + [negative_cycle[0]])
        )

        print("Negative-weight cycle detected.")
        print(f"Cycle: {cycle_text}")
        print(
            "Shortest-path distances are not well-defined because "
            "the cycle can reduce the path cost indefinitely."
        )
        return

    display_results(distance, predecessor, source)


if __name__ == "__main__":
    main()