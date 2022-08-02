class Flight:
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
        self.sold_business_seats = 0
        self.sold_economy_seats = 0

    def __repr__(self):
        return f"{self.flight_id} {self.airline_name} {self.origin} {self.destination} {self.departure_date} {self.departure_time} " \
               f"{self.arrival_date} {self.arrival_time} {int(self.seats) - (self.sold_economy_seats + self.sold_business_seats)}"

    def set_departure_info(self, departure_time: str, departure_date: str):
        self.departure_time = departure_time
        self.departure_date = departure_date

    def set_arrival_info(self, arrival_time: str, arrival_date: str):
        self.arrival_time = arrival_time
        self.arrival_date = arrival_date

    def get_departure_info(self, just_date= False):
        if just_date:
            return self.departure_date
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
        return self.flight_id

    def get_seats(self):
        return self.seats

    def update_seats(self, quantity, class_):
        if int(quantity) + int(self.sold_economy_seats) + int(self.sold_business_seats) > int(self.seats):
            raise Exception("Bad Request")
        if class_ == "economy":
            if int(self.sold_economy_seats) + int(quantity) > 0.75 * int(self.seats):
                raise Exception("Bad Request")
            self.sold_economy_seats = int(self.sold_economy_seats) + int(quantity)
        elif class_ == "business":
            if int(self.sold_business_seats) + int(quantity) > 0.25 * int(self.seats):
                raise Exception("Bad Request")
            self.sold_business_seats = int(self.sold_business_seats) + int(quantity)

    def get_connection_duration_with(self, other):
        other_date , other_time = other.get_departure_info()
        self_date , self_time = self.get_arrival_info()
        hours = 24 * (int(other_date) - int(self_date)) + (int(other_time.split(":")[0]) - int(self_time.split(":")[0]))
        minutes = int(other_time.split(":")[1]) - int(self_time.split(":")[1])
        if minutes < 0:
            return hours - 1 , minutes + 60
        return hours, minutes
