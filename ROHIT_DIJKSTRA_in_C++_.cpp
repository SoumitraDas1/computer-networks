#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <algorithm>
using namespace std;
struct Edge {
    int to;
    int weight;
};
void dijkstra(int startNode, int numNodes, const vector<vector<Edge>>& graph) {
    vector<int> dist(numNodes, INT_MAX);
    vector<int> parent(numNodes, -1);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    dist[startNode] = 0;
    pq.push({0, startNode});
    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if (d > dist[u]) continue;
        for (const auto& edge : graph[u]) {
            int v = edge.to;
            int weight = edge.weight;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
        for (int i = 0; i < numNodes; ++i) {
        cout << "Router " << i << "\t\t";
        if (dist[i] == INT_MAX) {
            cout << "Unreachable\tN/A\n";
        } else {
            cout << dist[i] << "\t\t";
                vector<int> path;
            for (int curr = i; curr != -1; curr = parent[curr]) {
                path.push_back(curr);
            }
            reverse(path.begin(), path.end());
            for (size_t j = 0; j < path.size(); ++j) {
                cout << path[j] << (j == path.size() - 1 ? "" : " -> ");
            }
            cout << "\n";
        }
    }
}
int main() {
    int numNodes = 6;
    vector<vector<Edge>> graph(numNodes);
    auto addLink = [&](int u, int v, int cost) {
        graph[u].push_back({v, cost});
        graph[v].push_back({u, cost});
    };
    addLink(0, 1, 4); 
    addLink(0, 2, 2);
    addLink(1, 2, 1);
    addLink(1, 3, 5);
    addLink(2, 3, 8);
    addLink(2, 4, 10);
    addLink(3, 4, 2); 
    addLink(3, 5, 6); 
    addLink(4, 5, 3); 
    int sourceRouter = 0;
    dijkstra(sourceRouter, numNodes, graph);
    return 0;
}
