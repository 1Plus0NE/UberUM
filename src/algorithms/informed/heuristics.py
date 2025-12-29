# Funções de heurística centralizadas
from typing import Optional
from graph.position import Position
from refuel_config import PRECO_BATERIA, PRECO_COMBUSTIVEL
from vehicle.vehicle_types import Eletric, Combustion, Hybrid, VehicleType

MAX_SPEED_KMH = 80.0  # Velocidade máxima esperada para estimativa de tempo
MAX_SPEED_MPS = MAX_SPEED_KMH / 3.6
COST_PER_KM = 0.50    # Custo por km (combustível/desgaste)
COST_PER_MIN = 0.20   # Custo por minuto (salário motorista/oportunidade)

def calculate_heuristic(pos1: Position, pos2: Position, criterion: str, vehicle_type: Optional[VehicleType] = None) -> float:
	"""
	Calcula a heurística h(n) baseada no critério escolhido.
	Para 'operational_cost', é obrigatório passar o tipo de veículo.
	"""
	dist_meters = pos1.distance_to(pos2)

	if criterion == 'distance':
		return dist_meters

	elif criterion == 'time':
		return dist_meters / MAX_SPEED_MPS

	elif criterion == 'cost':
		if vehicle_type is None:
			raise ValueError("Para a heurística de custo operacional, forneça o tipo de veículo.")
		dist_km = dist_meters / 1000.0
		if isinstance(vehicle_type, Eletric):
			energia_necessaria = vehicle_type.battery_consumption * dist_km  # kWh
			return energia_necessaria * PRECO_BATERIA
		elif isinstance(vehicle_type, Combustion):
			combustivel_necessario = vehicle_type.fuel_consumption * dist_km  # L
			return combustivel_necessario * PRECO_COMBUSTIVEL
		elif isinstance(vehicle_type, Hybrid):
			bateria_km = vehicle_type.current_battery / vehicle_type.battery_consumption if vehicle_type.battery_consumption > 0 else 0
			if dist_km <= bateria_km:
				energia_necessaria = vehicle_type.battery_consumption * dist_km
				return energia_necessaria * PRECO_BATERIA
			else:
				energia_necessaria = vehicle_type.battery_consumption * bateria_km
				combustivel_necessario = vehicle_type.fuel_consumption * (dist_km - bateria_km)
				return energia_necessaria * PRECO_BATERIA + combustivel_necessario * PRECO_COMBUSTIVEL
		else:
			return dist_km * COST_PER_KM

	return dist_meters
