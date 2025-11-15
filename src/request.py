from graph.position import Position

class Request:
    '''
        Represents a request of a client of an Uber
        Args:
            start_point: position where the client will be picked up in the graph
            end_point: position where the client will be dropped in the graph
            requested_time: when the uber was requested
            multiple_people: if the client allows the uber to gather other people for the same trip
    '''
    def __init__(self, start_point: Position, end_point: Position, requested_time, multiple_people: bool):
        self.start_point = start_point
        self.end_point = end_point
        self.requested_time = requested_time
        self.multiple_people = multiple_people
    