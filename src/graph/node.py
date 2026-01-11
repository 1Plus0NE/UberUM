from graph.position import Position

class Node:
    def __init__(self, id, position: Position, node_type="generic", capacity=0):
        """
        Representa um ponto da cidade.
        
        Args:
            id: Identificador único do nodo
            position: Posição no mapa (Position com x, y em metros)
            node_type: Tipo do nó ('pickup', 'charging', 'fuel', 'depot', 'generic')
            capacity: Capacidade (para estações ou zonas com limite de veículos)
        """
        self.id = id
        self.position = position
        self.node_type = node_type
        self.capacity = capacity

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def __repr__(self):
        return f"Node(id={self.id}, type={self.node_type}, pos=({self.position.x:.2f}, {self.position.y:.2f}))"