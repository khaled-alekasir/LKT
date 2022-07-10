class Ticket:
    def __init__(self, flight_id: int, airline_name: str, origin: str, destination: str, seats: str, cost: int):
        self.flight_id = flight_id
        self.airline_name = airline_name
        self.origin = origin
        self.destination = destination
        self.seats = seats
        self.cost = cost
        self.departure_time = None
        self.departure_date = None
        self.arrival_time = None
        self.arrival_date = None
        self.ticket_id = None

    def set_departure_info(self, departure_time: str, departure_date: str):
        self.departure_time = departure_time
        self.departure_date = departure_date

    def set_arrival_info(self, arrival_time: str, arrival_date: str):
        self.arrival_time = arrival_time
        self.arrival_date = arrival_date

    def get_departure_info(self):
        return self.departure_date , self.departure_time

    def get_arrival_info(self):
        return self.arrival_date , self.arrival_time

    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination

    def get_cost(self):
        return self.cost

    def get_airline(self):
        return self.airline_name

    def get_id(self):
        return self.id