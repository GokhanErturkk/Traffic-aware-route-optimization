from math import radians, sin, cos, sqrt, atan2


def generate_graph_with_distances():
    # Waypoints
    waypoints = [
        {"cityPoint": "A", "coordinates": (39.77978275602291, 30.51109313964844)},
        {"cityPoint": "D", "coordinates": (39.76460989601462, 30.509462356567386)},
        {"cityPoint": "B", "coordinates": (39.7779358040303, 30.52705764770508)},
        {"cityPoint": "E", "coordinates": (39.7652036794959, 30.52911758422852)},
        {"cityPoint": "C", "coordinates": (39.773252239280765, 30.54182052612305)},
        {"cityPoint": "F", "coordinates": (39.7624326461067, 30.543451309204105)},
    ]

    """
    A -- B -- C
    |    |
    D -- E -- F
    """
    # Define neighbors
    connections = {
        'A': ['B', 'D'],
        'B': ['A', 'C', 'E'],
        'C': ['B'],
        'D': ['A', 'E'],
        'E': ['B', 'D', 'F'],
        'F': ['E']
    }

    # Function to calculate Haversine distance
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371e3  # Earth's radius in meters
        phi1 = radians(lat1)
        phi2 = radians(lat2)
        delta_phi = radians(lat2 - lat1)
        delta_lambda = radians(lon2 - lon1)

        a = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c  # Distance in meters

    # Create a graph with distances
    graph = {}
    for point in waypoints:
        city = point["cityPoint"]
        graph[city] = {}
        
        for neighbor in connections[city]:
            neighbor_point = next(wp for wp in waypoints if wp["cityPoint"] == neighbor)
            distance = haversine_distance(
                point["coordinates"][0], point["coordinates"][1],
                neighbor_point["coordinates"][0], neighbor_point["coordinates"][1]
            )
            graph[city][neighbor] = distance

    return graph
