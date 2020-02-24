class User:

    def __init__(self, first_name, last_name, username, birthdate, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.birthdate = birthdate
        self.email = email
        self.password = password
        
    @property
    def email(self):
        return self.email
    
    @property
    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.first_name, self.last_name, self.email)