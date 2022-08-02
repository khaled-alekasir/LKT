class User:
    def __init__(self , username:str , password:str , credit:float = 0):
        self.username = username
        self.password = password
        self.credit = credit

    def __str__(self):
        return self.username + "  " + self.password

    def __repr__(self):
        return  self.username + "   " + self.password

    def __hash__(self):
        return hash(f"{self.username}{self.password}")

    def __eq__(self, other):
        if not isinstance(other , User):
            return False
        return self.username == other.username and self.password == other.password

    def add_credit(self, added_credit:float):
        self.credit = float(self.credit) + float(added_credit)

    def purchase(self, amount):
        if float(self.credit) < float(amount):
            raise Exception("Bad Request")
        self.credit = float(self.credit) - float(amount)

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

