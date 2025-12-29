from typing import List, Tuple
from graph.graph import Graph
from graph.position import Position
import heapq
from algorithms.informed.heuristics import calculate_heuristic

def greedy_bfs(start: Position, goal: Position, graph: Graph, criterion: str = 'cost') -> Tuple[float, float, List[int]]:
    start_node = graph.find_closest_node(start)
    goal_node = graph.find_closest_node(goal)
    
    open_set = []
    # Greedy usa apenas h(n) para ordenar
    h_start = calculate_heuristic(start_node.position, goal_node.position, criterion)
    heapq.heappush(open_set, (h_start, start_node))
    
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
            if not edge.get("open", True):
                continue
            neighbor = graph.get_node(edge["target"])
            if neighbor.id not in visited:
                came_from[neighbor.id] = current
                # Calcula heurística baseada no critério (ex: tempo estimado até ao fim)
                h_score = calculate_heuristic(neighbor.position, goal_node.position, criterion)
                heapq.heappush(open_set, (h_score, neighbor))
                
    return float('inf'), float('inf'), []