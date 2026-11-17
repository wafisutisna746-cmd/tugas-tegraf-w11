"""Dinic's max-flow algorithm (standalone).

Usage:  python dinic.py < sample/sample_case.txt
Input (stdin): first line "n m s t", then m lines "u v capacity" (0-indexed,
        '#' starts a comment).
Output: a single integer, the maximum flow.
Time:   O(V^2 E)
"""
import sys
from collections import deque


class FlowNetwork:
    """Residual graph; edge e and its reverse e ^ 1 are stored as a pair."""

    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.to, self.cap, self.orig = [], [], []

    def add_edge(self, u, v, c):
        self.adj[u].append(len(self.to))
        self.to.append(v); self.cap.append(c); self.orig.append(c)
        self.adj[v].append(len(self.to))
        self.to.append(u); self.cap.append(0); self.orig.append(0)

    def edge_flows(self):
        return [(self.to[e ^ 1], self.to[e], self.orig[e] - self.cap[e], self.orig[e])
                for e in range(0, len(self.to), 2)]


def read_network(stream):
    # Stops as soon as all m edges are read, so typing the input in a terminal
    # works without sending EOF (Ctrl-Z / Ctrl-D).
    tokens, need = [], None
    for line in stream:
        tokens += line.split("#")[0].split()
        if need is None and len(tokens) >= 4:
            need = 4 + 3 * int(tokens[1])
        if need is not None and len(tokens) >= need:
            break
    n, m, s, t = map(int, tokens[:4])
    net = FlowNetwork(n)
    for i in range(m):
        u, v, c = map(int, tokens[4 + 3 * i: 7 + 3 * i])
        net.add_edge(u, v, c)
    return net, s, t


def dinic(net, s, t):
    n, adj, to, cap = net.n, net.adj, net.to, net.cap
    total = 0
    while True:
        # 1) BFS builds the level graph
        level = [-1] * n
        level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for e in adj[u]:
                v = to[e]
                if cap[e] > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        if level[t] < 0:
            return total

        # 2) Blocking flow: iterative DFS with current-arc pointers
        it = [0] * n
        path, u = [], s
        while True:
            if u == t:
                b = min(cap[e] for e in path)
                for e in path:
                    cap[e] -= b
                    cap[e ^ 1] += b
                total += b
                path, u = [], s
                continue
            advanced = False
            while it[u] < len(adj[u]):
                e = adj[u][it[u]]
                v = to[e]
                if cap[e] > 0 and level[v] == level[u] + 1:
                    path.append(e)
                    u = v
                    advanced = True
                    break
                it[u] += 1
            if not advanced:
                if u == s:
                    break
                level[u] = -1  # dead end
                e = path.pop()
                u = to[e ^ 1]
                it[u] += 1


if __name__ == "__main__":
    net, s, t = read_network(sys.stdin)
    print(dinic(net, s, t))
