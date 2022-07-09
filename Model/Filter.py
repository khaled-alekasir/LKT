class Filter:
    def __int__(self):
        pass

    def filter(self, tickets_list: list):
        return tickets_list


class DestinationFilter(Filter):
    def __int__(self, from_:str, to_: str):
        self.from_ = from_
        self.to_ = to_

    def filter(self, ticket_list:list):
        new_list = list()
        for ticket in ticket_list:
            if self.from_ == ticket.get_origin() and self.to_ == ticket.get_destination():
                new_list.append(ticket)
        return new_list


class PriceFilter(Filter):
    def __int__(self, min_price:float, max_price:float):
        self.min_price = min_price
        self.max_price = max_price

    def filter(self, ticket_list:list):
        new_list = list()
        for ticket in ticket_list:
            if ticket.get_cost() <= self.max_price and ticket.get_cost >= self.min_price:
                new_list.append(ticket)
        return new_list


class AirlineFilter(Filter):
    def __int__(self, airline_name):
        self.airline_name = airline_name

    def filter(self, tickets_list: list):
        new_list = list()
        for ticket in tickets_list:
            if ticket.get_airline() == self.airline_name:
                new_list.append(ticket)
        return new_list