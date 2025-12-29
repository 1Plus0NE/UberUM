# Algoritmos disponíveis
from .uninformed.dfs import dfs
from .uninformed.bfs import bfs
from .uninformed.uniform_cost import uniform_cost_search
from .informed.a_star import a_star
from .informed.greedy import greedy_bfs

ALGORITHMS = {
    'dfs': dfs,
    'bfs': bfs,
    'uniform_cost': uniform_cost_search,
    'a_star': a_star,
    'greedy': greedy_bfs,
}
