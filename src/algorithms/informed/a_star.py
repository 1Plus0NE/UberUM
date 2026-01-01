"""
Implementação do algoritmo A* com suporte a múltiplos critérios de otimização:
- 'distance': Caminho mais curto (padrão)
- 'time': Caminho mais rápido (considera limites de velocidade e trânsito)
- 'cost': Menor custo operacional (combinação de distância e tempo)
"""
from typing import Any, List, Tuple, Optional
from graph.graph import Graph
from graph.position import Position
import heapq

# Importa preços de energia/combustível
from algorithms.informed.heuristics import calculate_heuristic

def get_edge_weight(edge: dict, criterion: str) -> float:
    """Retorna o peso g(n) da aresta baseado no critério."""
    if criterion == 'distance':
        return edge["distance"]
    elif criterion == 'time':
        return edge.get("time", 0.0)  # Tempo em segundos (já inclui trânsito)
    elif criterion == 'cost':
        # Custo Operacional = (Km * Custo_Km) + (Minutos * Custo_Min)
        dist_km = edge["distance"] / 1000.0
        time_min = edge.get("time", 0.0) / 60.0
        return (dist_km * COST_PER_KM) + (time_min * COST_PER_MIN)
    return edge["distance"]


def a_star(start: Position, goal: Position, graph: Graph, criterion: str = 'distance') -> Tuple[float, float, List[int]]:
    start_node = graph.find_closest_node(start)
    goal_node = graph.find_closest_node(goal)
    
    # Priority Queue armazena (f_score, node)
    open_set = []
    
    # Inicializa scores
    g_score = {node.id: float('inf') for node in graph.nodes}
    g_score[start_node.id] = 0
    
    h_start = calculate_heuristic(start_node.position, goal_node.position, criterion)
    f_score = {node.id: float('inf') for node in graph.nodes}
    f_score[start_node.id] = h_start
    
    heapq.heappush(open_set, (f_score[start_node.id], start_node))
    came_from = {}
    
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
            if not edge.get("open", True):
                continue
            neighbor = graph.get_node(edge["target"])
            # Calcula g(n) tentativo usando a função de peso correta
            weight = get_edge_weight(edge, criterion)
            tentative_g_score = g_score[current.id] + weight
            if tentative_g_score < g_score[neighbor.id]:
                came_from[neighbor.id] = current
                g_score[neighbor.id] = tentative_g_score
                h_score = calculate_heuristic(neighbor.position, goal_node.position, criterion)
                f_score[neighbor.id] = tentative_g_score + h_score
                heapq.heappush(open_set, (f_score[neighbor.id], neighbor))
                
    return float('inf'), float('inf'), []