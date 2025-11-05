from graph.node import Node
from graph.position import Position
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, directed=False):
        self.nodes = []
        self.edges = {}
        self.osm_to_internal = {} # usado para mapear o id OSM para o next_id 
        self.directed = directed
        self.next_id = 0

    def add_node(self, x, y, node_type="generic", capacity=0, osm_id=None):
        position = Position(x, y)
        node = Node(self.next_id, position, node_type=node_type, capacity=capacity)
        node.set_id(self.next_id)
        node.osm_id = osm_id

        self.nodes.append(node)
        self.edges[self.next_id] = []
        
        # Atualiza os dicionários de mapeamento
        if osm_id is not None:
            self.osm_to_internal[osm_id] = self.next_id

        self.next_id += 1
        return node

    def get_node(self, node_id):
        """Retorna o nó correspondente ao ID interno (int)."""
        if isinstance(node_id, int) and 0 <= node_id < len(self.nodes):
            return self.nodes[node_id]
        return None

    def add_edge(self, id1, id2, distance=None, time=None, traffic_factor=1.0, open=True):
        """
        Adiciona uma aresta entre dois nós (usando IDs internos).

        Args:
            id1, id2 (int): IDs internos do primeiro nó e do segundo nó
            distance (float): Distância em metros.
            time (float): Tempo estimado (em minutos, segundos, etc.).
            traffic_factor (float): Fator multiplicador do tempo devido ao trânsito.
            open (bool): Se a estrada está aberta. Default=True.
        """
        n1 = self.get_node(id1)
        n2 = self.get_node(id2)
        if not n1 or not n2: # nunca acontece mas quem sabe
            raise ValueError(f"Os nós {id1} e {id2} devem existir antes de criar uma aresta")

        # Calcula a distância se não for fornecida
        if distance is None:
            distance = n1.position.distance_to(n2.position)

        # Calcula o tempo se não fornecido, por omissão é estimimado 50 km/h
        if time is None:
            time = (distance / 50) * traffic_factor

        # Cria a aresta direta
        edge_info = {
            "target": id2,
            "distance": distance,
            "time": time,
            "traffic_factor": traffic_factor,
            "open": open
        }
        self.edges[id1].append(edge_info)

        # Cria a aresta reversa (i.e, contexto da estrada com dois sentidos)
        if not self.directed:
            reverse_info = {
                "target": id1,
                "distance": distance,
                "time": time,
                "traffic_factor": traffic_factor,
                "open": open
            }
        self.edges[id2].append(reverse_info)

    def plot(self, show_labels=True):
        """
        Desenha o grafo com cores e estilos de acordo com o tipo de nó e o estado das arestas.
        """
        node_colors = {
            "pickup": "green",
            "charging": "orange",
            "fuel": "red",
            "depot": "blue",
            "generic": "gray"
        }

        edge_colors = {
            "open": "black",         # normal
            "closed": "red",         # bloqueada
            "traffic": "orange"      # congestionada
        }

        plt.figure(figsize=(10, 8))

        # Desenhar as arestas
        for node_id, edges in self.edges.items():
            n1 = self.get_node(node_id)
            if not n1:
                continue

            for edge in edges:
                n2 = self.get_node(edge["target"])
                if not n2:
                    continue

                # Escolher cor e estilo com base no estado
                if not edge.get("open", True):
                    color = edge_colors["closed"]
                    style = "--"
                elif edge.get("traffic_factor", 1.0) > 1.3:
                    color = edge_colors["traffic"]
                    style = "-"
                else:
                    color = edge_colors["open"]
                    style = "-"

                plt.plot(
                    [n1.position.x, n2.position.x],
                    [n1.position.y, n2.position.y],
                    linestyle=style,
                    color=color,
                    linewidth=0.5 * edge.get("traffic_factor", 1.0),
                    alpha=0.8
                )

        # Desenhar os nós
        for node in self.nodes:
            color = node_colors.get(node.node_type, "black")
            size = 50 + (node.capacity * 5 if hasattr(node, "capacity") else 0)

            plt.scatter(node.position.x, node.position.y, color=color, s=size, zorder=3)
            if show_labels:
                plt.text(
                    node.position.x + 0.5,
                    node.position.y + 0.5,
                    str(node.id),
                    fontsize=7,
                    color="black",
                    zorder=4
                )

        plt.title("City Graph Representation (with dynamic edges)")
        plt.axis("equal")
        plt.axis("off")
        plt.show()