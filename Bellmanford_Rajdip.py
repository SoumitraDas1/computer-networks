def bellman_ford(graph, V, source):

    distance = [9999] * V
    distance[source] = 0

    # Relax edges V-1 times
    for i in range(V - 1):
        for u, v, w in graph:
            if distance[u] != 9999 and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w

    # Check for negative weight cycle
    for u, v, w in graph:
        if distance[u] != 9999 and distance[u] + w < distance[v]:
            print("Negative weight cycle exists")
            return

    print("Vertex\tDistance")

    for i in range(V):
        print(i, "\t", distance[i])


graph = [
    (0, 1, 4),
    (0, 2, 5),
    (1, 2, -3),
    (2, 3, 4),
    (3, 1, -2)
]

V = 4
source = 0

bellman_ford(graph, V, source)