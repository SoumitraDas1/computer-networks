def bellman_ford(V, graph, source):

    INF = 9999
    distance = [INF] * V
    distance[source] = 0

    # Relax all edges V-1 times
    for i in range(V - 1):
        updated = False

        for u, v, w in graph:
            if distance[u] != INF and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                updated = True

        # Stop early if no distance was updated
        if not updated:
            break

    # Check for negative weight cycle
    for u, v, w in graph:
        if distance[u] != INF and distance[u] + w < distance[v]:
            print("\nNegative weight cycle exists!")
            return

    # Display shortest distances
    print("\nVertex\tDistance")

    for i in range(V):
        if distance[i] == INF:
            print(i, "\tINF")
        else:
            print(i, "\t", distance[i])


# Taking input from user
V = int(input("Enter number of vertices: "))
E = int(input("Enter number of edges: "))

graph = []

print("\nEnter edges in the format: source destination weight")

for i in range(E):
    u, v, w = map(int, input(f"Edge {i + 1}: ").split())
    graph.append((u, v, w))

source = int(input("\nEnter source vertex: "))

bellman_ford(V, graph, source)