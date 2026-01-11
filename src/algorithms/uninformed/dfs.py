from typing import Any, List, Tuple
from graph.graph import Graph
from graph.position import Position

def dfs(start: Position, goal: Position, graph: Graph) -> Tuple[float, float, List[int]]:
    start_node = graph.find_closest_node(start)
    goal_node = graph.find_closest_node(goal)
    stack = [(start_node, [start_node.id])]
    visited = set()
    visited.add(start_node.id)  # Marca como visitado ao adicionar à stack
    
    while stack:
        current, path = stack.pop()
        if current.id == goal_node.id:
            total_distance, total_time = graph.calculate_path_metrics(path)
            return total_distance, total_time, path
        
        for edge in graph.edges[current.id]:
            if not edge.get("open", True):
                continue
            neighbor = graph.get_node(edge["target"])
            if neighbor.id not in visited:
                visited.add(neighbor.id)  # Marca como visitado ANTES de adicionar à stack
                stack.append((neighbor, path + [neighbor.id]))
    return float('inf'), float('inf'), []
