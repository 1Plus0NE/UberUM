from enum import Enum
from graph.position import Position
from request import Request

class Vehicle_Status(Enum):
    ''' Represents the current status of the vehicle '''
    IDLE = 0
    TRAVELING = 1
    REFUELING = 2
    RECHARGING = 3

class Eletric:
    ''' 
        Represents an eletric vehicle 
        Includes attributes for battery capacity, battery consumption and its current battery
    '''
    def __init__(self, battery_capacity: float, battery_consumption: float, current_battery: float):
        
        self.battery_capacity = battery_capacity # kWh
        self.battery_consumption = battery_consumption
        self.current_battery = current_battery

    ''' Updates current's vehicle battert given a distance in meters to travel'''
    def consumption(self, distance: float):
        distance = distance/1000 # convert to km
        wasted_battery = self.battery_consumption * distance 
        self.fuel_capacity -= wasted_battery

    ''' Given a distance in meters, determines if the vehicle has enough battery to travel the given distance'''
    def hasEnoughBattery(self, distance: float) -> bool:
        return self.consumption(distance) > self.battery_capacity

class Combustion:
    ''' 
        Represents a combustion vehicle 
        Includes attributes for fuel capacity, fuel consumption and its current fuel
    '''
    def __init__(self, fuel_capacity: float, fuel_consumption: float, current_fuel: float):
        
        self.fuel_capacity = fuel_capacity # Liters
        self.fuel_consumption = fuel_consumption 
        self.current_fuel = current_fuel

    ''' Updates current's vehicle fuel given a distance in meters to travel'''
    def consumption(self, distance: float):
        distance = distance/1000 # convert to km
        wasted_fuel = self.fuel_consumption * distance 
        self.fuel_capacity -= wasted_fuel

    ''' Given a distance in meters, determines if the vehicle has enough fuel to travel the given distance'''
    def hasEnoughFuel(self, distance: float):
        return self.consumption(distance) > self.fuel_capacity

class Hybrid:
    ''' 
        Represents a hybrid vehicle 
        Includes attributes from an eletric vehicle and a combustion vehicle
    '''
    def __init__(self, battery_capacity: float, battery_consumption: float, fuel_capacity: float, 
                 fuel_consumption: float, current_battery: float, current_fuel: float):
        
        self.battery_capacity = battery_capacity
        self.battery_consumption = battery_consumption
        self.fuel_capacity = fuel_capacity
        self.fuel_consumption = fuel_consumption

        self.current_fuel = current_fuel
        self.current_battery = current_battery
        
class Vehicle:
    '''
        Represents an individual vehicle
    '''
    def __init__(self, id: int, name: str, vehicle_type, capacity: int, driver: str, status: Vehicle_Status, start_point: Position):
        self.id = id
        self.name = name
        self.vehicle_type = vehicle_type
        self.capacity = capacity
        self.driver = driver
        self.status = status

        # posição atual para desenho (intermediária enquanto se move)
        self.current_position: Position = start_point
        self.current_node_id: int | None = None  # ID do nó onde o táxi está (se estiver num nó)

        # informação de passageiros / pedido atual
        self.passengers = 0
        self.current_request = None

        # Fase da viagem: 'to_pickup' ou 'to_dropoff'
        self.phase: str | None = None
        
        # Caminho (path) a seguir: lista de IDs de nós
        self.path: list[int] = []
        self.path_to_dropoff: list[int] = []  # guarda caminho para fase 2
        
        # Movimento ao longo de arestas
        self.current_edge_from: int | None = None  # nó de origem da aresta atual
        self.current_edge_to: int | None = None    # nó de destino da aresta atual
        self.edge_travel_time: float = 0          # tempo total desta aresta (minutos)
        self.time_remaining_on_edge: float = 0    # tempo restante nesta aresta (minutos)
        
        # Referência ao grafo (necessária para obter posições dos nós)
        self.graph = None

    def assign(self, request: Request, 
               path_to_pickup: list[int] | None, path_to_dropoff: list[int] | None, graph):
        """
        Atribui um pedido ao táxi com os caminhos calculados.
        """
        self.current_request = request
        self.phase = 'to_pickup'
        self.status = Vehicle_Status.TRAVELING
        self.passengers = 0
        self.graph = graph
        
        # Atualiza request
        request.assigned_vehicle = self
        request.status = 'assigned'  # Atribuído mas ainda não chegou ao pickup
        
        # Guarda caminhos
        if path_to_pickup:
            self.path = path_to_pickup.copy()
        else:
            self.path = []
        
        if path_to_dropoff:
            self.path_to_dropoff = path_to_dropoff.copy()
        else:
            self.path_to_dropoff = []
        
        # Inicia movimento na primeira aresta
        self.advance_to_next_edge()

    def advance_to_next_edge(self):
        """Avança para a próxima aresta do caminho."""
        if len(self.path) >= 2:
            self.current_edge_from = self.path[0]
            self.current_edge_to = self.path[1]
            
            # Busca tempo da aresta no grafo
            edges = self.graph.edges.get(self.current_edge_from, [])
            edge_time = 0
            for edge in edges:
                if edge["target"] == self.current_edge_to:
                    edge_time = edge["time"]
                    break
            
            self.edge_travel_time = edge_time
            self.time_remaining_on_edge = edge_time
            self.path.pop(0)  # remove o nó atual (já estamos a sair dele)
            
        elif len(self.path) == 1:
            # Chegou ao último nó do caminho atual
            self.current_node_id = self.path[0]
            node = self.graph.get_node(self.current_node_id)
            if node:
                self.current_position = node.position
            
            # Se acabou fase to_pickup, muda para to_dropoff
            if self.phase == 'to_pickup':
                self.phase = 'to_dropoff'
                self.passengers = self.current_request.passengers if self.current_request else 0
                # Atualiza status do request
                if self.current_request:
                    self.current_request.status = 'picked_up'
                self.path = self.path_to_dropoff.copy()
                self.advance_to_next_edge()
            else:
                # Acabou viagem completa
                if self.current_request:
                    self.current_request.status = 'completed'
                self.status = Vehicle_Status.IDLE
                self.phase = None
                self.passengers = 0
                self.current_request = None
                self.path = []
                self.current_edge_from = None
                self.current_edge_to = None
        else:
            # Sem caminho, fica parado
            self.status = Vehicle_Status.IDLE

    def update_status(self, current_time: int, time_step: int = 1):
        """
        Atualiza o estado do táxi a cada tick.
        
        Args:
            current_time: Tempo atual da simulação em minutos
            time_step: Quantos minutos avançam neste tick (padrão: 1)
        """
        if self.status != Vehicle_Status.TRAVELING:
            return
        
        if self.current_edge_from is None or self.current_edge_to is None:
            return
        
        # Decrementa tempo restante na aresta usando time_step
        self.time_remaining_on_edge -= time_step
        
        if self.time_remaining_on_edge <= 0:
            # Chegou ao fim da aresta atual
            self.current_node_id = self.current_edge_to
            node = self.graph.get_node(self.current_node_id)
            if node:
                self.current_position = node.position
            
            # Avança para próxima aresta
            self.advance_to_next_edge()
        else:
            # Ainda está a meio da aresta - interpola posição
            if self.edge_travel_time > 0:
                frac = 1 - (self.time_remaining_on_edge / self.edge_travel_time)
                frac = max(0.0, min(1.0, frac))
                
                # Obtém posições dos nós
                node_from = self.graph.get_node(self.current_edge_from)
                node_to = self.graph.get_node(self.current_edge_to)
                
                if node_from and node_to:
                    x1, y1 = node_from.position.x, node_from.position.y
                    x2, y2 = node_to.position.x, node_to.position.y
                    nx = x1 + frac * (x2 - x1)
                    ny = y1 + frac * (y2 - y1)
                    self.current_position = Position(nx, ny)
