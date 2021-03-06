import csv
import shelve
import sys
from Model.Flight import Flight
from Model.User import User
from Model.Filter import *

class Expedia:
    def __init__(self):
        self.logged_in_user = None
        self.user_ticket_map = dict()  #user -> (flight_object, id, quantity, class:str, class_:str, paid:float)
        self.flights = list()
        self.users = list()
        self.filter = Filter()
        with shelve.open("DataBase\\WebDatabase") as db:
            if len(db.keys()) == 0:
                self.__read_csv()
            else:
                self.__read_database()

    def __str__(self):
        return f"users = {self.users} , tickets = {self.flights}"

    def __read_csv(self, file_path = ""):
        with open("D:\\CS\\I\\Advanced Programming\\Final Project\\flights.csv") as csv_file:
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

    def __read_data_base(self):
        with open("DataBase\\WebDatabase") as db:
            self.user_ticket_map = db["tickets"]
            self.flights = db["flights"]
            self.users = db["users"]

    def __find_flight_by_id(self, id):
        for flight in self.flights:
            if flight.get_id() == id:
                return flight
        raise Exception("Bad Request")

    def signup(self, username, password):
        new_user = User(username , password)
        self.users.append(new_user)
        self.user_ticket_map[new_user] = list()
        self.logged_in_user = new_user

    def login(self, username, password):
        for user in self.users:
            if user.get_username() == username and user.get_password() == password:
                self.logged_in_user = user
                break
        raise Exception("Not found")

    def logout(self):
        assert self.logged_in_user != None , "Peremission denied"
        self.logged_in_user = None
        self.filter = Filter()

    def add_credit(self, amount):
        assert self.logged_in_user != None, "Peremission denied"
        self.logged_in_user.add_credit(amount)

    def get_flights(self):
        assert self.logged_in_user != None, "Peremission denied"

        for flight in self.filter.filter(self.flights):
            print(flight)

    def get_flight_by_id(self, id:int):
        assert self.logged_in_user != None, "Peremission denied"

        for flight in self.flights:
            if flight.get_id() == id:
                return self.user_ticket_map[self.logged_in_user]
        raise Exception("Empty")

    def buy_ticket(self, flight_id, quantity, class_, type):
        assert self.logged_in_user != None, "Peremission denied"

        rate = 1 if class_ == "economy" else 2.5
        flight = self.__find_flight_by_id(flight_id)
        flight.update_seats(quantity, class_)
        paid = quantity * flight.get_cost() * rate
        self.logged_in_user.purchase(paid)
        self.user_ticket_map[self.logged_in_user].append((flight, self.curr_id, class_, type, paid))

    def show_loggedin_users_tickets(self):
        for ticket in self.user_ticket_map[self.logged_in_user]:
            print(ticket)

    def show_user_ticket(self, id):
        assert self.logged_in_user != None, "Peremission denied"
        assert len(self.user_ticket_map[self.logged_in_user]) > 0 , "Empty"

        for ticket in self.user_ticket_map[self.logged_in_user]:
            if ticket[1] == id:
                print(self.user_ticket_map[self.logged_in_user])
        raise Exception("Bad request")

    def cancel_ticket(self, id):
        assert self.logged_in_user != None, "Peremission denied"

        for ticket in self.user_ticket_map[self.logged_in_user]:
            if ticket[1] == id:
                if type == "nonrefundable":
                    raise Exception("Bad Request")
                else:
                    ticket[0].update_seats(-1 * ticket[2])
                    self.logged_in_user.add_credit(0.5 * ticket[5])
                    self.user_ticket_map[self.logged_in_user].remove(ticket)
                    return
        raise Exception("Bad Request")

    def add_filter(self, filter):
        self.filter = filter

    def get_connecting_flights(self, from_, to_):
        connecting_flights = list()
        in_between_flights = [flight for flight in self.flights if flight.get_destination() ==to_]
        print(in_between_flights)
        for flight1 in self.flights:
            if flight1.get_origin() != from_:
                continue
            for flight2 in in_between_flights:
                if flight1.get_destination() != flight2.get_origin():
                    continue
                duration = flight1.get_connection_duration_with(flight2)
                if ((duration[0] == 15 and duration[1] ==0) or duration[0]< 14) and duration[0] >= 0:
                    connecting_flights.append((flight1, flight2))
        return connecting_flights

    def get_cheapest_flights(self, from_, to_):
        pass