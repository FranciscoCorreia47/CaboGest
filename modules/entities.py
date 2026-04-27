from db_config import connection, cursor

class People:
    def __init__(self, id, f_name, l_name, email):
        self.id = id
        self.f_name = f_name
        self.l_name = l_name
        self.email = email


class Clients(People):
    def __init__(self, id, f_name, l_name, email, nationality, birth_date):
        super().__init__(id, f_name, l_name, email)
        self.nationality = nationality
        self.birth_date = birth_date
    
    def make_reservation(self):
        pass

    def check_out(self):
        pass


class Users(People):
    def __init__(self, id, f_name, l_name, email, password, role):
        super().__init__(id, f_name, l_name, email)
        self.password = password
        self.role = role
    
    def add_client():
        pass

    def add_room():
        pass

    def login():
        pass

    def register_reservation():
        pass


class Reservations:
    def __init__(self, id, start_date, end_date, status, total_price):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.total_price = total_price


class Rooms:
    def __init__(self, id, bed_qty, category, occupied, description, price_per_night):
        self.id = id
        self.bed_qty = bed_qty
        self.category = category
        self.occupied = occupied
        self.description = description
        self.price_per_night = price_per_night

    def update_status():
        pass        