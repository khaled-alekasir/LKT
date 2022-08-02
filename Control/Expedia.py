import csv
import shelve
import os
import sys

from Model.Flight import Flight
from Model.User import User
from Model.Filter import *
from collections import Counter

DATA_BASE_PATH = os.getcwd() + "\\DataBase\\WebDatabase"

class Expedia:
    def __init__(self):
        self.logged_in_user = None
        self.user_ticket_map = dict()  #user -> (flight_object, id, quantity, class:str, type:str, paid:float)
        self.flights = list()
        self.users = list()
        self.filter = Filter()
        with shelve.open(DATA_BASE_PATH) as db:
            if len(db.keys()) == 0:
                self.__read_csv()
                self.curr_id = 1
            else:
                self.__read_database()

    def __str__(self):
        return f"users = {self.users} , tickets = {self.flights}"

    def __read_csv(self, file_path = ""):
        with open(sys.argv[1]) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # print(csv_reader)
            id = 1
            for row in csv_reader:
                # print(row)
                flight = Flight(id, row["airline"], row["origin"], row["destination"], row["seats"], row["cost"])
                flight.set_departure_info(row["departure_time"], row["departure_date"])
                flight.set_arrival_info(row["arrival_time"], row["arrival_date"])
                self.flights.append(flight)
                id += 1

    def __read_database(self):
        with shelve.open(DATA_BASE_PATH) as db:
            self.user_ticket_map = db["tickets"]
            self.flights = db["flights"]
            self.users = db["users"]
            self.curr_id = db["curr_id"]

    def __find_flight_by_id(self, flight_id):
        for flight in self.flights:
            if int(flight.get_id()) == int(flight_id):
                return flight
        raise Exception("Bad Request")

    def __get_direct_flights(self, from_, to_)->list:
        list_to_be_returned = list()
        for flight in self.flights:
            if flight.get_origin() == from_ and flight.get_destination() == to_:
                list_to_be_returned.append(flight)
        return list_to_be_returned

    def update_database(self):
        with shelve.open(DATA_BASE_PATH) as db:
            db["tickets"] = self.user_ticket_map
            db["flights"] = self.flights
            db["users"] = self.users
            db["curr_id"] = self.curr_id

    def signup(self, username, password):
        assert self.logged_in_user == None, "Bad Request"

        for user in self.users:
            if user.get_username() == username :
                raise Exception ("Bad Request")
        new_user = User(username , password)
        self.users.append(new_user)
        self.user_ticket_map[new_user] = list()
        self.logged_in_user = new_user

    def login(self, username, password):
        assert self.logged_in_user == None, "Bad Request"

        for user in self.users:
            if user.get_username() == username and user.get_password() == password:
                self.logged_in_user = user
                return
        raise Exception("Bad Request")

    def logout(self):
        assert self.logged_in_user != None , "Peremission Denied"

        self.logged_in_user = None
        self.filter = Filter()

    def add_credit(self, amount):
        assert self.logged_in_user != None, "Peremission Denied"
        self.logged_in_user.add_credit(amount)

    def get_flights(self):
        assert self.logged_in_user != None, "Peremission Denied"
        assert len(self.filter.filter(self.flights)) > 0 , "Empty"

        return self.filter.filter(self.flights)

    def get_flight_by_id(self, id:int):
        assert self.logged_in_user != None, "Peremission Denied"

        for flight in self.flights:
            if flight.get_id() == id:
                return self.user_ticket_map[self.logged_in_user]
        raise Exception("Empty")

    def buy_ticket(self, flight_id, quantity, class_, type):
        assert self.logged_in_user != None, "Peremission Denied"

        rate = 1 if class_ == "economy" else 2.5
        flight = self.__find_flight_by_id(flight_id)
        flight.update_seats(quantity, class_)
        paid = int(quantity) * float(flight.get_cost()) * float(rate)
        self.logged_in_user.purchase(paid)
        self.user_ticket_map[self.logged_in_user].append([flight, self.curr_id, quantity, class_, type, paid])
        self.curr_id += 1

    def get_loggedin_users_tickets(self):
        assert self.logged_in_user != None, "Peremission Denied"
        assert len(self.user_ticket_map[self.logged_in_user]) > 0, "Empty"

        return self.user_ticket_map[self.logged_in_user]

    def get_user_ticket(self, id):
        assert self.logged_in_user != None, "Peremission Denied"
        assert len(self.user_ticket_map[self.logged_in_user]) > 0 , "Empty"

        for ticket in self.user_ticket_map[self.logged_in_user]:
            if ticket[1] == id:
                return ticket
        raise Exception("Bad request")

    def cancel_ticket(self, id):
        assert self.logged_in_user != None, "Peremission denied"

        for ticket in self.user_ticket_map[self.logged_in_user]:
            print(ticket)
            if int(ticket[1]) == int(id):
                if ticket[4] == "nonrefundable":
                    raise Exception("Bad Request")
                else:
                    print("canceling...")
                    ticket[0].update_seats(-1 * int(ticket[2]), ticket[3])
                    self.logged_in_user.add_credit(0.5 * int(ticket[5]))
                    self.user_ticket_map[self.logged_in_user].remove(ticket)
                    return
        raise Exception("Bad Request")

    def add_filter(self, filter):
        self.filter = filter

    def delete_filters(self):
        self.filter = Filter()

    def get_connecting_flights(self, from_, to_)->list:
        assert self.logged_in_user != None, "Peremission denied"

        connecting_flights = list()
        in_between_flights = [flight for flight in self.flights if flight.get_destination() ==to_]
        for flight1 in self.flights:
            if flight1.get_origin() != from_:
                continue
            for flight2 in in_between_flights:
                if flight1.get_destination() != flight2.get_origin():
                    continue
                duration = flight1.get_connection_duration_with(flight2)
                if ((duration[0] == 15 and duration[1] ==0) or duration[0]< 14) and duration[0] >= 0:
                    connecting_flights.append((flight1, flight2))
        assert len(connecting_flights)>0 , "Empty"

        return connecting_flights

    def get_cheapest_flights(self, from_, to_, dep_date):
        assert self.logged_in_user != None, "Peremission denied"

        direct_flights = self.__get_direct_flights(from_, to_)
        connected_flights = self.get_connecting_flights(from_, to_)

        direct_flights = list(filter(lambda flight: flight.get_departure_info(True) == dep_date, direct_flights))
        connected_flights = list(filter(lambda tup: tup[0].get_departure_info(True) == dep_date, connected_flights))

        assert len(direct_flights) > 0 or len(connected_flights) >0, "Not Found"

        cheapest_direct_flight = min(direct_flights, key=lambda flight: flight.get_cost(), default=None)
        cheapest_connected_flight = min(connected_flights,key= lambda tup:tup[0].get_cost() + tup[0].get_cost(), default=None)

        if len(connected_flights) == 0 :
            return cheapest_direct_flight

        direct_cost = cheapest_direct_flight.get_cost() if cheapest_direct_flight != None else float('inf')
        connected_cost = cheapest_connected_flight[0].get_cost() + cheapest_connected_flight[1].get_cost()

        return cheapest_direct_flight if direct_cost <= connected_cost else cheapest_connected_flight

    def get_overall_report(self):
        info = dict()
        destinations = list()
        airlines = list()
        for user in self.users:
            for ticket in self.user_ticket_map[user]:
                destinations += [ticket[0].get_destination()] * int(ticket[2])
                airlines += [ticket[0].get_airline()] *  int(ticket[2])
        costs = [float(flight.get_cost()) for flight in self.flights]
        dest_counter = Counter(destinations)
        airline_counter = Counter(airlines)
        info["average_flight_cost"] = float(round(sum(costs)/len(costs), 2))
        info["min_flight_cost"] = float(round(min(costs),2))
        info["max_flight_cost"] = float(round(max(costs),2))
        info["most_popular_destination"] = " ".join([dest[0] for dest in dest_counter.most_common(1)])
        info["top_airlines"] = " ".join(list(sorted([airline[0] for airline in airline_counter.most_common(3)])))

        return info