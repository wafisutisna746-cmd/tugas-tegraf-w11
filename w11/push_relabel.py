"""Push-Relabel max-flow algorithm, FIFO selection rule (standalone).

Usage:  python push_relabel.py < sample/sample_case.txt
Input (stdin): first line "n m s t", then m lines "u v capacity" (0-indexed,
        '#' starts a comment).
Output: a single integer, the maximum flow.
Time:   O(V^3)
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


def push_relabel(net, s, t):
    n, adj, to, cap = net.n, net.adj, net.to, net.cap
    height = [0] * n
    excess = [0] * n
    cur = [0] * n
    height[s] = n
    q = deque()

    # Initial preflow: saturate every edge leaving the source
    for e in adj[s]:
        c = cap[e]
        if c > 0:
            v = to[e]
            cap[e] -= c
            cap[e ^ 1] += c
            excess[v] += c
            excess[s] -= c
            if v != t and v != s and excess[v] == c:
                q.append(v)

    while q:
        u = q.popleft()
        while excess[u] > 0:
            if cur[u] == len(adj[u]):
                # relabel: one above the lowest residual neighbour
                height[u] = 1 + min(height[to[e]] for e in adj[u] if cap[e] > 0)
                cur[u] = 0
                continue
            e = adj[u][cur[u]]
            v = to[e]
            if cap[e] > 0 and height[u] == height[v] + 1:
                d = min(excess[u], cap[e])  # push
                cap[e] -= d
                cap[e ^ 1] += d
                excess[u] -= d
                excess[v] += d
                if v != s and v != t and excess[v] == d:
                    q.append(v)
            else:
                cur[u] += 1
    return excess[t]


if __name__ == "__main__":
    net, s, t = read_network(sys.stdin)
    print(push_relabel(net, s, t))
