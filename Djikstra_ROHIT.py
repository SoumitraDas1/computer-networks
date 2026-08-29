import heapq
def dijkstra(graph, start_node):
    distances = {node: float("inf") for node in graph}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start_node)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighborimport heapq

def dijkstra(graph, start):
    # Distance from start to every vertex
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    # Priority queue: (distance, vertex)
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Ignore outdated entries
        if current_distance > distances[current_vertex]:
            continue

        # Check all neighbours
        for neighbour, weight in graph[current_vertex]:
            distance = current_distance + weight

            # If a shorter path is found
            if distance < distances[neighbour]:
                distances[neighbour] = distance
                heapq.heappush(priority_queue, (distance, neighbour))

    return distances


# Graph represented using an adjacency list
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2)],
    'E': [('C', 10), ('D', 2)]
}

# Find shortest paths from A
start = 'A'
result = dijkstra(graph, start)

print("Shortest distances from", start)

for vertex, distance in result.items():
    print(vertex, ":", distance)
]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances, previous_nodes
def get_shortest_path(previous_nodes, target_node):
    path = []
    current = target_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    return path
network_topology = {
    "Router_A": {"Router_B": 4, "Router_C": 2},
    "Router_B": {"Router_A": 4, "Router_C": 1, "Router_D": 5},
    "Router_C": {"Router_A": 2, "Router_B": 1, "Router_D": 8, "Router_E": 10},
    "Router_D": {"Router_B": 5, "Router_C": 8, "Router_E": 2, "Router_F": 6},
    "Router_E": {"Router_C": 10, "Router_D": 2, "Router_F": 3},
    "Router_F": {"Router_D": 6, "Router_E": 3},
}
source_router = "Router_A"
distances, previous_nodes = dijkstra(network_topology, source_router)
print(f"=== Routing Table for Source: {source_router} ===")
print(f"{'Destination':<15} | {'Cost (ms)':<10} | {'Shortest Path'}")
print("-" * 45)
for destination in network_topology:
    path = get_shortest_path(previous_nodes, destination)
    path_str = " -> ".join(path)
    print(f"{destination:<15} | {distances[destination]:<10} | {path_str}")
