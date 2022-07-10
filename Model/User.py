class User:
    def __init__(self , username:str , password:str , credit:float = 0):
        self.username = username
        self.password = password
        self.credit = credit

    def __str__(self):
        return self.username + "  " + self.password

    def __repr__(self):
        return  self.username + "   " + self.password

    def add_credit(self, added_credit:float):
        self.credit += added_credit

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

