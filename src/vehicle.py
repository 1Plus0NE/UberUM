from enum import Enum
from graph.position import Position

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

        self.start_point = start_point       # por definir a posição por defeito dos veículos
        self.end_point = None                # vai receber o seu end_point depois de um pedido de um cliente
        self.current_position = start_point
        self.passengers = 0