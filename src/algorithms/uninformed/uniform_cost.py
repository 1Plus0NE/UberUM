from typing import Any, List, Tuple
from graph.graph import Graph
from graph.position import Position
import heapq

def uniform_cost_search(start: Position, goal: Position, graph: Graph) -> Tuple[float, float, List[int]]:
    start_node = graph.find_closest_node(start)
    goal_node = graph.find_closest_node(goal)
    open_set = []
    heapq.heappush(open_set, (0, start_node, [start_node.id]))
    visited = set()
    while open_set:
        cost, current, path = heapq.heappop(open_set)
        if current.id == goal_node.id:
            total_distance, total_time = graph.calculate_path_metrics(path)
            return total_distance, total_time, path
        if current.id in visited:
            continue
        visited.add(current.id)
        for edge in graph.edges[current.id]:
            if not edge.get("open", True):
                continue
            neighbor = graph.get_node(edge["target"])
            if neighbor.id not in visited:
                heapq.heappush(open_set, (cost + edge["distance"], neighbor, path + [neighbor.id]))
    return float('inf'), float('inf'), []
