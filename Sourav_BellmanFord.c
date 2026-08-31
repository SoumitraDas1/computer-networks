#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#define INF INT_MAX
struct Edge {
    int src, dest, weight;
};
struct Graph {
    int V;
    int E;
    struct Edge* edge;
};
struct Graph* createGraph(int V, int E) {
    struct Graph* graph = (struct Graph*)malloc(sizeof(struct Graph));
    graph->V = V;
    graph->E = E;
    graph->edge = (struct Edge*)malloc(graph->E * sizeof(struct Edge));
    return graph;
}
void printSolution(int dist[], int V) {
    printf("\nVertex\tDistance from Source\n");
    for (int i = 0; i < V; i++) {
        if (dist[i] == INF)
            printf("%d\tINF\n", i);
        else
            printf("%d\t%d\n", i, dist[i]);
    }
}
void printPath(int parent[], int j) {
    if (parent[j] == -1) {
        printf("%d", j);
        return;
    }
    printPath(parent, parent[j]);
    printf(" -> %d", j);
}
void bellmanFord(struct Graph* graph, int src) {
    int V = graph->V;
    int E = graph->E;
    int dist[V];
    int parent[V];
    for (int i = 0; i < V; i++) {
        dist[i] = INF;
        parent[i] = -1;
    }
    dist[src] = 0;
    for (int i = 1; i <= V - 1; i++) {
        for (int j = 0; j < E; j++) {
            int u = graph->edge[j].src;
            int v = graph->edge[j].dest;
            int weight = graph->edge[j].weight;
            if (dist[u] != INF && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
            }
        }
    }
    for (int j = 0; j < E; j++) {
        int u = graph->edge[j].src;
        int v = graph->edge[j].dest;
        int weight = graph->edge[j].weight;
        if (dist[u] != INF && dist[u] + weight < dist[v]) {
            printf("\nGraph contains a negative weight cycle. "
                   "Bellman-Ford solution is not applicable.\n");
            return;
        }
    }
    printSolution(dist, V);
    printf("\nShortest Paths from source %d:\n", src);
    for (int i = 0; i < V; i++) {
        if (i == src) continue;
        if (dist[i] == INF) {
            printf("%d: No path exists\n", i);
        } else {
            printf("%d: ", i);
            printPath(parent, i);
            printf("  (Cost = %d)\n", dist[i]);
        }
    }
}
int main() {
    int V, E;
    printf("=== Bellman-Ford Algorithm (Network Routing) ===\n\n");
    printf("Enter number of vertices (routers/nodes): ");
    scanf("%d", &V);
    printf("Enter number of edges (links): ");
    scanf("%d", &E);
    struct Graph* graph = createGraph(V, E);
    printf("\nEnter each edge as: source destination weight\n");
    printf("(Vertices are numbered from 0 to %d)\n", V - 1);
    for (int i = 0; i < E; i++) {
        printf("Edge %d: ", i + 1);
        scanf("%d %d %d", &graph->edge[i].src,
                           &graph->edge[i].dest,
                           &graph->edge[i].weight);
    }
    int src;
    printf("\nEnter source vertex (router): ");
    scanf("%d", &src);
    if (src < 0 || src >= V) {
        printf("Invalid source vertex!\n");
        return 1;
    }
    bellmanFord(graph, src);
    free(graph->edge);
    free(graph);
    return 0;
}
