import math

class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: 'Position') -> float:
        """Calcula a distância euclidiana entre duas posições."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return f"Position(x={self.x:.2f}, y={self.y:.2f})"