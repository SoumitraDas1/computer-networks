class Edge:
    """Represents a directed weighted edge."""

    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight


class BellmanFord:
    """Bellman-Ford shortest path algorithm."""

    INF = float("inf")

    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []

    def add_edge(self, src, dest, weight):
        """Add a directed edge."""
        self.edges.append(Edge(src, dest, weight))

    def bellman_ford(self, source):
        """Find shortest paths from source and detect negative cycles."""

        distance = [self.INF] * self.vertices
        parent = [-1] * self.vertices

        distance[source] = 0

        # Relax all edges V-1 times.
        for _ in range(self.vertices - 1):
            updated = False

            for edge in self.edges:
                u = edge.src
                v = edge.dest
                w = edge.weight

                if distance[u] != self.INF and distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    parent[v] = u
                    updated = True

            # Stop early when no update occurs.
            if not updated:
                break

        # Check for a negative-weight cycle.
        for edge in self.edges:
            u = edge.src
            v = edge.dest
            w = edge.weight

            if distance[u] != self.INF and distance[u] + w < distance[v]:
                print(
                    "\nGraph contains a negative weight cycle.\n"
                    "Bellman-Ford cannot compute correct shortest paths."
                )
                return

        self.print_solution(distance, parent, source)

    def get_path(self, parent, node):
        """Return the path from the source to the specified node."""

        path = []
        current = node

        while current != -1:
            path.append(current)
            current = parent[current]

        path.reverse()
        return " -> ".join(map(str, path))

    def print_solution(self, distance, parent, source):
        """Print the routing table."""

        print(f"\nRouting Table for Node {source}")
        print("Destination\tCost\tPath")
        print("-" * 45)

        for i in range(self.vertices):
            if distance[i] == self.INF:
                print(f"{i}\t\tINF\tUnreachable")
            else:
                path = self.get_path(parent, i)
                print(f"{i}\t\t{distance[i]}\t{path}")


def main():
    # Create graph with 5 vertices: 0, 1, 2, 3, 4.
    graph = BellmanFord(5)

    # Same graph as the original Java program.
    graph.add_edge(0, 1, 6)
    graph.add_edge(0, 2, 7)
    graph.add_edge(1, 2, 8)
    graph.add_edge(1, 3, 5)
    graph.add_edge(1, 4, -4)
    graph.add_edge(2, 3, -3)
    graph.add_edge(2, 4, 9)
    graph.add_edge(3, 1, -2)
    graph.add_edge(4, 3, 7)
    graph.add_edge(4, 0, 2)

    # Calculate shortest paths from node 0.
    graph.bellman_ford(0)


if __name__ == "__main__":
    main()