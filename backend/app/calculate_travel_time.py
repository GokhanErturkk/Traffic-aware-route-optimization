def calculate_shortest_path(graph, all_paths, velocity_dict, camera_placements):
    shortest_path = None
    shortest_time = float('inf')
    
    for path_info in all_paths:
        total_distance = path_info[0]  # First element is the total distance
        path = path_info[1]           # Second element is the path as a list of nodes
        
        total_time = 0
        for i in range(len(path) - 1):
            # Get the nodes for the current segment
            node_start = path[i]
            node_end = path[i + 1]
            
            # Get the distance between the two nodes
            distance = graph[node_start][node_end]
            
            # Get the camera placement key
            camera_key = f"{node_start}{node_end}"
            
            # Get the velocity for this segment
            if camera_key in camera_placements:
                camera_id = camera_placements[camera_key]
                velocity = velocity_dict.get(camera_id, 1)  # Default velocity is 1 if not found
            else:
                velocity = 1  # Default velocity if camera_key is missing
            
            # Calculate time for this segment and add to total time
            segment_time = distance / velocity
            total_time += segment_time
        
        # Update shortest path if this one is faster
        if total_time < shortest_time:
            shortest_time = total_time
            shortest_path = path
    
    return shortest_path
