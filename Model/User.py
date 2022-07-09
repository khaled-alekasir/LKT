class User:
    def __int__(self , username:str , password:str , credit:float = 0):
        self.username = username
        self.password = password
        self.credit = credit
    def add_credit(self, added_credit:float):
        self.credit += added_credit
    