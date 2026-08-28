import java.util.*;
public class BellmanFord {
    static class Edge {
        int src, dest, weight;
        Edge(int src, int dest, int weight) {
            this.src = src;
            this.dest = dest;
            this.weight = weight;
        }
    }
    static final int INF = Integer.MAX_VALUE;
    int V; 
    int E; 
    List<Edge> edges;
    BellmanFord(int V, int E) {
        this.V = V;
        this.E = E;
        edges = new ArrayList<>();
    }
    void addEdge(int src, int dest, int weight) {
        edges.add(new Edge(src, dest, weight));
    }
    void bellmanFord(int src) {
        int[] dist = new int[V];
        int[] parent = new int[V];
        Arrays.fill(dist, INF);
        Arrays.fill(parent, -1);
        dist[src] = 0;
        for (int i = 1; i <= V - 1; i++) {
            for (Edge edge : edges) {
                int u = edge.src;
                int v = edge.dest;
                int w = edge.weight;
                if (dist[u] != INF && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    parent[v] = u;
                }
            }
        }
        for (Edge edge : edges) {
            int u = edge.src;
            int v = edge.dest;
            int w = edge.weight;
            if (dist[u] != INF && dist[u] + w < dist[v]) {
                System.out.println("Graph contains a negative weight cycle. " +
                        "Bellman-Ford cannot compute correct shortest paths.");
                return;
            }
        }
        printSolution(dist, parent, src);
    }
    void printSolution(int[] dist, int[] parent, int src) {
        System.out.println("\nRouting Table for Node " + src);
        System.out.println("Destination\tCost\tNext Hop / Path");
        System.out.println("---------------------------------------------");
        for (int i = 0; i < V; i++) {
            System.out.print(i + "\t\t");
            if (dist[i] == INF) {
                System.out.println("INF\tUnreachable");
            } else {
                System.out.print(dist[i] + "\t");
                printPath(parent, i);
                System.out.println();
            }
        }
    }
    void printPath(int[] parent, int node) {
        if (parent[node] == -1) {
            System.out.print(node);
            return;
        }
        printPath(parent, parent[node]);
        System.out.print(" -> " + node);
    }
    public static void main(String[] args) {
        int V = 5; 
        int E = 8; 
        BellmanFord graph = new BellmanFord(V, E);
        graph.addEdge(0, 1, 6);
        graph.addEdge(0, 2, 7);
        graph.addEdge(1, 2, 8);
        graph.addEdge(1, 3, 5);
        graph.addEdge(1, 4, -4);
        graph.addEdge(2, 3, -3);
        graph.addEdge(2, 4, 9);
        graph.addEdge(3, 1, -2);
        graph.addEdge(4, 3, 7);
        graph.addEdge(4, 0, 2);
        graph.bellmanFord(0);
    }
}
