from modules.db_config import connection, cursor
from datetime import date, time, datetime, timedelta

class Rooms:
    def __init__(self, id, bed_qty: int, category, type, price_per_night: float = 0.0, occupied: int = 0, description = None):
        self.__id = id
        self.__bed_qty = bed_qty
        self.__category = category
        self.__type = type
        self.__occupied = occupied
        self.description = description
        self.price_per_night = price_per_night
        self.add_room()
    
    @property
    def id(self):
        return self.__id

    @property
    def occupied(self):
        return self.__occupied
    
    @occupied.setter
    def update_status(self, status: int):
        if status not in (0, 1):
            raise ValueError(f"Room Status can only be 0 for free or 1 for occupied, got {status}")
        else:
            self.__occupied = status
        con = connection
        curs = cursor

        query = "UPDATE rooms SET occupied = %d WHERE id = %d"
        params = (self.occupied(), self.id())

        curs.execute(query, params)
        con.commit()

        curs.close()
        con.close()
    
    @property
    def bed_qty(self):
        return self.__bed_qty

    def add_room(self):
        con = connection
        curs = cursor

        query = "INSERT INTO rooms(bed_qty, category, type, description, price_per_night) VALUES (%d, %s, %s, %s, %f)"
        params = (self.bed_qty, self.category, self.type, self.description, self.price_per_night)
        
        curs.execute(query, params)
        con.commit()

        curs.close()
        con.close()


class People:
    def __init__(self, id, f_name, l_name, email):
        self.__id = id
        self._f_name = f_name
        self._l_name = l_name
        self._email = email

    @property
    def id(self):
        return self.__id


class Clients(People):
    def __init__(self, id, f_name, l_name, email, nationality, birth_date):
        super().__init__(id, f_name, l_name, email)
        self.nationality = nationality
        self.birth_date = birth_date
        self.add_client()

    def add_client(self):
        con = connection
        curs = cursor

        query = "INSERT INTO clients(f_name, l_name, email, birth_date, nationality) VALUES (%s, %s, %s, %s, %s)"
        params = (self._f_name, self._l_name, self._email, self.birth_date, self.nationality)
        
        curs.execute(query, params)
        con.commit()

        curs.close()
        con.close()


class Users(People):
    def __init__(self, id, f_name, l_name, email, password, role):
        super().__init__(id, f_name, l_name, email)
        self.__password = password
        self.role = role

    def add_user(self):
        con = connection
        curs = cursor

        query = "INSERT INTO users(f_name, l_name, email, password, role) VALUES (%s, %s, %s, %s, %s)"
        params = (self._f_name, self._l_name, self._email, self.__password, self.role)
        
        curs.execute(query, params)
        con.commit()

        curs.close()
        con.close()


class Reservations:
    def __init__(self, id, client_id: int, room_id: int, start_date: datetime, end_date: datetime, status: str, total_price: float):
        self.__id = id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.total_price = total_price
        self.__client_id = client_id
        self.__room_id = room_id

    @property
    def id(self):
        return self.__id
    
    def add_reservation(self, start_date: datetime, end_date: datetime):
        con = connection
        curs = cursor

        query = "INSERT INTO reservations(client_id, room_id, start_date, end_date) VALUES (%d, %d, %s, %s)"
        params = (self.__client_id, self.__room_id, start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'))
        curs.execute(query, params)
        con.commit()

        curs.close()
        con.close()

    def update_reservation(self, status: str):
        con = connection
        curs = cursor

        query = "UPDATE reservations SET status = %s WHERE id = %d AND status = %s"
        params = (status, self.id(), self.status)
        curs.execute(query, params)
        con.commit()

        curs.close()
        con.close()