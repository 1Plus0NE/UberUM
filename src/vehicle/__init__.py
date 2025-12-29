"""
Package de veículos - exporta classes principais.
"""
from vehicle.vehicle import Vehicle, Vehicle_Status
from vehicle.vehicle_types import VehicleType, Eletric, Combustion, Hybrid

__all__ = [
    'Vehicle',
    'Vehicle_Status',
    'VehicleType',
    'Eletric',
    'Combustion',
    'Hybrid',
]
