import csv
import sys
from Model.Ticket import Ticket
from Model.User import User

class Expedia:
    def __init__(self):
        self.logged_in_user = None
        self.user_ticket_map = dict()
        self.tickets = list()
        self.users = list()
        self.__read_csv()

    def __str__(self):
        return f"users = {self.users} , tickets = {self.tickets}"

    def __read_csv(self, file_path = ""):
        with open("D:\\CS\\I\\Advanced Programming\\Final Project\\flights.csv") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # print(csv_reader)
            id = 1
            for row in csv_reader:
                # print(row)
                ticket = Ticket(id, row["airline"], row["origin"], row["destination"], row["seats"], row["cost"])
                ticket.set_departure_info(row["departure_time"], row["departure_date"])
                ticket.set_arrival_info(row["arrival_time"], row["arrival_date"])
                self.tickets.append(ticket)
                id += 1

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

    def add_credit(self, amount):
        assert self.logged_in_user != None, "Peremission denied"
        self.logged_in_user.add_credit(amount)

    def get_flights(self):
        assert self.logged_in_user != None, "Peremission denied"
        for ticket in self.user_ticket_map[self.logged_in_user]:
            print(ticket)

    def get_flight_by_id(self, id:int):
        assert self.logged_in_user != None, "Peremission denied"
        for ticket in self.user_ticket_map[self.logged_in_user]:
            if ticket.get_id() == id:
                return ticket
        raise Exception("Empty")

    