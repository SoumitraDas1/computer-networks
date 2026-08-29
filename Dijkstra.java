import java.util.*;

public class Dijkstra {

    static final int INF = Integer.MAX_VALUE;

    public static void dijkstra(int[][] graph, int source) {
        int n = graph.length;

        int[] distance = new int[n];
        boolean[] visited = new boolean[n];

        // Initialize distances
        Arrays.fill(distance, INF);
        distance[source] = 0;

        for (int i = 0; i < n - 1; i++) {

            // Find the unvisited vertex with minimum distance
            int u = -1;

            for (int j = 0; j < n; j++) {
                if (!visited[j] && (u == -1 || distance[j] < distance[u])) {
                    u = j;
                }
            }

            // If no reachable vertex is found
            if (u == -1 || distance[u] == INF) {
                break;
            }

            visited[u] = true;

            // Update distances of adjacent vertices
            for (int v = 0; v < n; v++) {
                if (graph[u][v] != 0 &&
                    !visited[v] &&
                    distance[u] != INF &&
                    distance[u] + graph[u][v] < distance[v]) {

                    distance[v] = distance[u] + graph[u][v];
                }
            }
        }

        // Print shortest distances
        System.out.println("Vertex\tDistance from Source");

        for (int i = 0; i < n; i++) {
            System.out.println(i + "\t\t" + distance[i]);
        }
    }

    public static void main(String[] args) {

        int[][] graph = {
            {0, 4, 0, 0, 0, 0, 0, 8, 0},
            {4, 0, 8, 0, 0, 0, 0, 11, 0},
            {0, 8, 0, 7, 0, 4, 0, 0, 2},
            {0, 0, 7, 0, 9, 14, 0, 0, 0},
            {0, 0, 0, 9, 0, 10, 0, 0, 0},
            {0, 0, 4, 14, 10, 0, 2, 0, 0},
            {0, 0, 0, 0, 0, 2, 0, 1, 6},
            {8, 11, 0, 0, 0, 0, 1, 0, 7},
            {0, 0, 2, 0, 0, 0, 6, 7, 0}
        };

        int source = 0;

        dijkstra(graph, source);
    }
}