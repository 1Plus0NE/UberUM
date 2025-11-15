from enum import Enum

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
    def __init__(self, battery_capacity, battery_consumption, current_battery):
        
        self.battery_capacity = battery_capacity
        self.battery_consumption = battery_consumption
        self.current_battery = current_battery

class Combustion:
    ''' 
        Represents a combustion vehicle 
        Includes attributes for fuel capacity, fuel consumption and its current fuel
    '''
    def __init__(self, fuel_capacity, fuel_consumption, current_fuel):
        
        self.fuel_capacity = fuel_capacity
        self.fuel_consumption = fuel_consumption
        self.current_fuel = current_fuel

class Hybrid:
    ''' 
        Represents a hybrid vehicle 
        Includes attributes from an eletric vehicle and a combustion vehicle
    '''
    def __init__(self, battery_capacity, battery_consumption, fuel_capacity, fuel_consumption, current_battery, current_fuel):
        
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
    def __init__(self, id, name, vehicle_type, capacity, driver, status):
    
        self.id = id
        self.name = name
        self.vehicle_type = vehicle_type
        self.capacity = capacity
        self.driver = driver          
        self.status = status

        self.start_point = None
        self.end_point = None
        self.passengers = 0
        self.current_position = None  # posição atual/intermediária
        self.request_start_time = None
        self.estimated_arrival_time = None

    def assign(self, request, current_time, estimated_arrival_time):
        self.start_point = request['origin']
        self.end_point = request['destination']
        self.current_position = self.start_point
        self.status = Vehicle_Status.TRAVELING
        self.request_start_time = current_time
        self.estimated_arrival_time = estimated_arrival_time
        self.passengers = request.get('passengers', 1)
        self.current_request = request

    def update_status(self, current_time):
        if self.status != Vehicle_Status.TRAVELING or not self.end_point:
            return

        # Se já chegou ao destino
        if current_time >= self.estimated_arrival_time:
            self.current_position = self.end_point
            self.status = Vehicle_Status.IDLE
            self.passengers = 0
            self.start_point = self.end_point
            self.end_point = None
            self.current_request = None
            self.request_start_time = None
            self.estimated_arrival_time = None
            return

        # Atualiza posição intermediária (movimento linear entre start_point e end_point)
        total_time = self.estimated_arrival_time - self.request_start_time
        elapsed = current_time - self.request_start_time
        if total_time > 0 and self.start_point and self.end_point:
            ratio = elapsed / total_time
            sx, sy = self.start_point.x, self.start_point.y
            ex, ey = self.end_point.x, self.end_point.y
            nx = sx + (ex - sx) * ratio
            ny = sy + (ey - sy) * ratio
            self.current_position = type(self.start_point)(nx, ny)