import heapq

def dijkstra_all_paths(graph, start, target):
    # Priority queue: stores (distance, node, path)
    pq = []
    heapq.heappush(pq, (0, start, [start]))  # Start with the source node (distance 0)

    # To store all paths and their distances
    paths = []

    while pq:
        current_distance, current_node, path = heapq.heappop(pq)

        # If the target is reached, store the path
        if current_node == target:
            paths.append((current_distance, path))
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node].items():
            if neighbor not in path:  # Avoid cycles
                new_distance = current_distance + weight
                heapq.heappush(pq, (new_distance, neighbor, path + [neighbor]))

    # Sort paths by distance
    paths.sort(key=lambda x: x[0])
    return paths

# Example usage
graph = {
    "A": {"B": 1379.626291509768, "D": 1692.8919725081037},
    "D": {"A": 1692.8919725081037, "E": 1681.2844708922053},
    "B": {"A": 1379.626291509768, "C": 1364.8912297087995, "E": 1426.651869576661},
    "E": {"B": 1426.651869576661, "D": 1681.2844708922053, "F": 1263.315310130033},
    "C": {"B": 1364.8912297087995},
    "F": {"E": 1263.315310130033}
}

start_node = "A"
target_node = "C"
all_paths = dijkstra_all_paths(graph, start_node, target_node)

print (all_paths)