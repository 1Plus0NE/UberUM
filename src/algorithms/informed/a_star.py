from typing import Any, List, Tuple
from graph.graph import Graph
from graph.position import Position
import heapq

def heuristic(pos1: Position, pos2: Position) -> float:
    return pos1.distance_to(pos2)

def a_star(start: Position, goal: Position, graph: Graph) -> Tuple[float, float, List[int]]:
    start_node = graph.find_closest_node(start)
    goal_node = graph.find_closest_node(goal)
    open_set = []
    heapq.heappush(open_set, (0, start_node))
    came_from = {}
    g_score = {node.id: float('inf') for node in graph.nodes}
    g_score[start_node.id] = 0
    f_score = {node.id: float('inf') for node in graph.nodes}
    f_score[start_node.id] = heuristic(start_node.position, goal_node.position)

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
        for edge in graph.edges[current.id]:
            neighbor = graph.get_node(edge["target"])
            tentative_g_score = g_score[current.id] + edge["distance"]
            if tentative_g_score < g_score[neighbor.id]:
                came_from[neighbor.id] = current
                g_score[neighbor.id] = tentative_g_score
                f_score[neighbor.id] = tentative_g_score + heuristic(neighbor.position, goal_node.position)
                heapq.heappush(open_set, (f_score[neighbor.id], neighbor))
    return float('inf'), float('inf'), []
