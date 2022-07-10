from Control.Expedia import Expedia
class ConsoleView:
    def __init__(self, control):
        self.control = control

    def run(self):
        while True:
            command = input()
            temp_command = command.split(" ")

            #loggin and loggout commands!

            if command.startswith("POST signup"):
                self.control.signup(temp_command[temp_command.index("username")+1], temp_command[temp_command.index("password")+1])

            elif command.startswith("POST login"):
                self.control.login(temp_command[temp_command.index("username")+1], temp_command[temp_command.index("password")+1])

            elif command.startswith("POST logout"):
                self.control.logout()

            #Buy or cancel ticket commands

            elif command.startswith("POST wallet"):
                self.control.add_credit(int(temp_command[temp_command.index("amount")+1]))

            elif command == "GET flights":
                self.control.get_flights()

            elif command.startswith("GET flight"):
                print(self.control.get_flight_by_id(int(temp_command[temp_command.index(("id")+1)])))

            elif command.startswith("POST tickets"):
                infos = ["flight", "quantity", "class", "class_"]
                flight_id, quantity, class_, type = (temp_command[temp_command.index(info)] for info in infos)
                self.control.buy_ticket(flight_id, quantity, class_, type)

            elif command == "GET tickets":
                self.control.show_loggedin_users_tickets()

            elif command.startswith("GET tickets"):
                self.control.show_user_ticket(int(temp_command[temp_command.index("id")])+1)

            elif command.startswith(("DELETE tickets")):
                self.control.cancel_ticket(temp_command[temp_command.index("id")])+1)

            #filter commands

            elif command.startswith("POST filters ? from"):
                pass



expedia = Expedia()
c = ConsoleView(expedia)
c.run()