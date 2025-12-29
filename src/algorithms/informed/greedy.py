from typing import Any, List, Tuple
from graph.graph import Graph
from graph.position import Position
import heapq

def heuristic(pos1: Position, pos2: Position) -> float:
    return pos1.distance_to(pos2)

def greedy_bfs(start: Position, goal: Position, graph: Graph) -> Tuple[float, float, List[int]]:
    start_node = graph.find_closest_node(start)
    goal_node = graph.find_closest_node(goal)
    open_set = []
    heapq.heappush(open_set, (heuristic(start_node.position, goal_node.position), start_node))
    came_from = {}
    visited = set()
    while open_set:
        _, current = heapq.heappop(open_set)
        if current.id == goal_node.id:
            path = []
            while current.id in came_from:
                path.append(current.id)
                current = came_from[current.id]
            path.append(start_node.id)
            path.reverse()
            total_distance, total_time = graph.calculate_path_metrics(path)
            return total_distance, total_time, path
        visited.add(current.id)
        for edge in graph.edges[current.id]:
            neighbor = graph.get_node(edge["target"])
            if neighbor.id not in visited:
                came_from[neighbor.id] = current
                heapq.heappush(open_set, (heuristic(neighbor.position, goal_node.position), neighbor))
    return float('inf'), float('inf'), []
