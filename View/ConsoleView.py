from Control.Expedia import Expedia
from Model.Filter import *


class ConsoleView:
    def __init__(self, control):
        self.control = control

    def __print_ticket(self, ticket):
        flight = ticket[0]
        depart_date, depart_time = flight.get_departure_info()
        arrival_date, arrival_time = flight.get_arrival_info()
        print(f"{ticket[1]} {flight.get_id()} {flight.get_airline()} {ticket[2]} {flight.get_origin()} "
              f"{flight.get_destination()} {depart_date} {depart_time} {arrival_date} {arrival_time} "
              f"{ticket[3]} {ticket[4]} {ticket[5]}")

    def __print_connecting_flights(self,tickets):
        flight1 , flight2 = tickets
        arr_date1, arr_time1 = flight1.get_arrival_info()
        dep_date1, dep_time1 = flight1.get_departure_info()
        arr_date2, arr_time2 = flight2.get_arrival_info()
        dep_date2, dep_time2 = flight2.get_departure_info()
        hours , mins = flight1.get_connection_duration_with(flight2)

        print(f"Flight1: {flight1.get_airline()} {flight1.get_origin()} {flight1.get_destination} {dep_date1} {dep_time1}"
              f"{arr_date1} {arr_time1} {flight1.seats()} {flight1.get_cost()}")

        print(f"Flight2: {flight2.get_airline()} {flight2.get_origin()} {flight2.get_destination} {dep_date2} {dep_time2}"
              f"{arr_date2} {arr_time2} {flight2.seats()} {flight2.get_cost()}")

        print(f"* Connection duration {hours}h {mins}m, Total cost: {flight1.get_cost + flight2.get_cost()}")
    def __print_cheapest_ticket(self, tickets):
        if isinstance(tickets, tuple):
            total_cost = 0
            for ticket in tickets:
                total_cost += int(ticket.get_cost())
                print(ticket)
            print("Total cost: ", total_cost)
        else:
            self.__print_ticket(tickets)
            print("Total cost: ", tickets.get_cost())

    def __print_overall_report(self, infos):
        for key in infos.keys():
            print(key, " : ", infos[key])

    def run(self):
        while True:
            try:
                command = input()
                temp_command = command.split(" ")

                #loggin and loggout commands!

                if command.startswith("POST signup"):
                    self.control.signup(temp_command[temp_command.index("username")+1], temp_command[temp_command.index("password")+1])
                    print("OK")
                elif command.startswith("POST login"):
                    self.control.login(temp_command[temp_command.index("username")+1], temp_command[temp_command.index("password")+1])
                    print("OK")
                elif command.startswith("POST logout"):
                    self.control.logout()
                    print("OK")
                #Buy or cancel ticket commands

                elif command.startswith("POST wallet"):
                    self.control.add_credit(int(temp_command[temp_command.index("amount")+1]))
                    print("OK")

                elif command == "GET flights":
                    for flight in self.control.get_flights():
                        print(flight)

                elif command.startswith("GET flight"):
                    print(self.control.get_flight_by_id(int(temp_command[temp_command.index(("id")+1)])))

                elif command.startswith("POST tickets"):
                    infos = ["flight", "quantity", "class", "type"]
                    flight_id, quantity, class_, type = (temp_command[temp_command.index(info)+1] for info in infos)
                    self.control.buy_ticket(flight_id, quantity, class_, type)
                    print("OK")

                elif command == "GET tickets":
                    assert self.control.logged_in_user != None, "Peremission Denied"
                    for ticket in self.control.get_loggedin_users_tickets():
                        self.__print_ticket(ticket)

                elif command.startswith("GET tickets"):
                    self.__print_ticket(self.control.get_user_ticket(int(temp_command[temp_command.index("id")+1])))

                elif command.startswith(("DELETE tickets")):
                    self.control.cancel_ticket(temp_command[temp_command.index("id")+1])
                    print("OK")
                #filter commands

                elif command.startswith("POST filters ?") and "from" in command:
                    from_, to_ = temp_command[temp_command.index("from")+1] , temp_command[temp_command.index("to")+1]
                    self.control.add_filter(DestinationFilter(from_ , to_))
                    print("OK")

                elif command.startswith("POST filters ?") and "min_price" in command:
                    min, max = temp_command[temp_command.index("min_price")+1], temp_command[temp_command.index("max_price")+1]
                    self.control.add_filter(PriceFilter(float(min), float(max)))
                    print("OK")

                elif command.startswith("POST filters ?") and "airline" in command:
                    airline_name = temp_command[temp_command.index("airline")+1]
                    self.control.add_filter(AirlineFilter(airline_name))
                    print("OK")

                elif command.startswith("DELETE filters"):
                    self.control.delete_filters()

                elif command.startswith("GET connecting_flights ?"):
                    from_, to_ = temp_command[temp_command.index("from") + 1], temp_command[temp_command.index("to") + 1]
                    self.__print_connecting_flights(self.control.get_connecting_flights(from_, to_))

                elif command.startswith("GET cheapest_flight"):
                    infos = ["from", "to", "departure_date"]
                    from_, to_, dep_date = (temp_command[temp_command.index(info) + 1] for info in infos)
                    self.__print_cheapest_ticket(self.control.get_cheapest_flights(from_, to_, dep_date))

                elif command == "GET overall_report":
                    self.__print_overall_report(self.control.get_overall_report())

                self.control.update_database()
            except Exception as e:
                print(e)
