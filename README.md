# Graph Theory Network Flow Group Homework

## Identity
GROUP 8

|    NRP     |           Nama             |
| :--------: |       :------------:       |
| 5025251260 | Aqilah Ibrahim             |
| 5025251161 | Rizqi Arya Kuskhilbyano    |
| 5025251009 | Athar Rozy Rasyidan        |
| 5025251017 | Wafi Fawwaz Sutisna        |

## Algorithm

Both algorithms solve the **maximum flow problem**: given a directed graph where every edge has a capacity, a source `s` and a sink `t`, find the largest amount of flow that can be sent from `s` to `t` without exceeding any edge capacity. Neither is Ford-Fulkerson; both are improvements on the idea of augmenting along paths in a residual graph.

Both programs share the same data structure: a residual graph in which every edge `e` is stored together with its reverse edge `e ^ 1`. Pushing `d` units along `e` decreases `cap[e]` by `d` and increases `cap[e ^ 1]` by `d`, which lets flow be "undone" later.

### Dinic's Algorithm
Dinic's algorithm repeatedly finds *blocking flows* in a layered view of the residual graph, instead of augmenting one arbitrary path at a time.

- **Build the level graph.** A BFS from the source assigns each vertex its distance (level) from `s`, using only edges that still have residual capacity. If the sink is unreachable, no augmenting path exists and the algorithm stops with the maximum flow.
- **Find a blocking flow.** A DFS from the source sends flow only along edges that go from level `i` to level `i + 1`. Current-arc pointers (`it[u]`) make sure an edge that is saturated or leads to a dead end is never examined again in the same phase.
- **Repeat.** After the blocking flow is found, the level graph is rebuilt on the updated residual graph. The distance from `s` to `t` strictly increases after every phase, so there are at most `V` phases.

Because flow is only sent along shortest paths (by edge count), each phase is cheap and the number of phases is bounded by the number of vertices.

**Time complexity:** `O(V² E)`

### Push-Relabel Algorithm (FIFO selection rule)
Push-Relabel works differently from path-based algorithms. It never looks for a whole `s`-`t` path. Instead it keeps a *preflow*, where vertices are allowed to hold more flow coming in than going out (called *excess*), and pushes that excess locally toward the sink.

- **Initialize.** Every vertex gets a height of 0, except the source which gets height `V`. All edges leaving the source are saturated, which gives its neighbours some excess.
- **Push.** A vertex `u` with excess pushes flow along a residual edge `(u, v)` only if `height[u] = height[v] + 1`, i.e. strictly "downhill" by one step.
- **Relabel.** If `u` still has excess but no admissible edge, its height is raised to one more than its lowest residual neighbour.
- **FIFO rule.** Vertices with excess are kept in a queue and processed in first-in-first-out order, until the queue is empty. At that point the excess that has reached the sink is the maximum flow.

The height function acts as an estimate of the distance to the sink, and since the source sits at height `V`, any excess that cannot reach the sink eventually flows back toward the source instead of getting stuck.

**Time complexity:** `O(V³)`

### Comparison

| | Dinic | Push-Relabel (FIFO) |
| :-- | :-- | :-- |
| Approach | Augment along shortest paths in phases | Push excess locally, raise heights |
| Intermediate state | Always a valid flow | A preflow (excess allowed) |
| Key structure | Level graph (BFS) + blocking flow (DFS) | Height labels + FIFO queue |
| Time complexity | O(V² E) | O(V³) |

## Prerequisites
- Python 3.6 or newer
- No external libraries are required, the programs only use the Python standard library (`sys`, `collections`)
- Works on Linux, macOS, and Windows

## Instructions

1. Make sure `dinic.py`, `push_relabel.py` and the `sample/` folder are in the same folder.

2. Run an algorithm by feeding the input file through standard input:
```
python dinic.py < sample/sample_case.txt
python push_relabel.py < sample/sample_case.txt
```
On Linux/macOS use `python3` if `python` is not available.

3. To test with a different network, edit `sample/sample_case.txt` (or point to another file) using the format:
```
n m s t
u v capacity
u v capacity
...
```
- The first line holds the number of vertices `n`, the number of edges `m`, the source `s` and the sink `t`.
- Then follow `m` lines, one directed edge per line, from `u` to `v` with the given integer `capacity`.
- Vertices are numbered from `0` to `n - 1`.
- Everything after a `#` on a line is treated as a comment and ignored.

4. The output is a single integer: the maximum flow from `s` to `t`.

You can also type the input directly into the terminal (just run `python dinic.py` and enter the lines). The program stops reading once all `m` edges are entered, so there is no need to send EOF.

## Results

### Sample input
The sample is a 6-vertex network with source `0` and sink `5`.

```
# n m s t
6 10 0 5
# u v capacity
0 1 16
0 2 13
1 2 10
2 1 4
1 3 12
3 2 9
2 4 14
4 3 7
3 5 20
4 5 4
```

### Dinic's
```
$ python dinic.py  sample/sample_case.txt
```


Dinic's builds a level graph with BFS, pushes a blocking flow through it, and repeats until the sink is no longer reachable, arriving at a maximum flow of 23.

### Push-Relabel
```
$ python push_relabel.py  sample/sample_case.txt
```

Push-Relabel saturates the edges leaving the source, then pushes and relabels vertices in FIFO order until no vertex other than the source and sink holds excess, arriving at the same maximum flow of 23.

Both algorithms agree on the result, which matches the known maximum flow for this network.


### AI Disclosure
https://share.gemini.google/15Y0l9QI5tUT
