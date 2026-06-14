from modules.db_config import connection
from datetime import date, time, datetime, timedelta
import re

RESERVATION_STATUSES = [
    "checked_in",
    "checked_out",
    "transfered",
    "canceled",
    "active",
]


def normalize_reservation_status(status: str):
    if not isinstance(status, str):
        return "checked_in"
    normalized = status.strip().lower()
    if normalized in RESERVATION_STATUSES:
        return normalized
    return "checked_in"


class Rooms:
    def __init__(self, id, bed_qty: int, category, type, price_per_night: float = 0.0, occupied: int = 0, description = None):
        self.__id = id
        self.__bed_qty = bed_qty
        self.__category = category
        self.__type = type
        self.__occupied = occupied
        self.description = description
        self.price_per_night = price_per_night
        
    @property
    def id(self):
        return self.__id

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value):
        try:
            if value not in ["Regular", "With View"]:
                raise ValueError(f"Room Category can only be 'Regular' or 'With View', got {value}")
            self.__category = value
            con = connection
            curs = connection.cursor()

            query = "UPDATE rooms SET category = %s WHERE id = %s"
            params = (self.__category.lower(), self.__id)

            curs.execute(query, params)
            con.commit()

            curs.close()
        except ValueError as e:
            print(e)

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        try:
            if value not in ["Suite", "Single", "Double"]:
                raise ValueError(f"Room Type can only be 'Suite', 'Single' or 'Double', got {value}")
            self.__type = value
            con = connection
            curs = connection.cursor()

            query = "UPDATE rooms SET type = %s WHERE id = %s"
            params = (self.__type.lower(), self.__id)

            curs.execute(query, params)
            con.commit()

            curs.close()
        except ValueError as e:
            print(e)

    @property
    def occupied(self):
        return self.__occupied

    @occupied.setter
    def occupied(self, status: int):
        try:
            if status not in (0, 1):
                raise ValueError(f"Room Status can only be 0 for free or 1 for occupied, got {status}")
            self.__occupied = status
            con = connection
            curs = connection.cursor()

            query = "UPDATE rooms SET occupied = %s WHERE id = %s"
            params = (self.__occupied, self.__id)

            curs.execute(query, params)
            con.commit()

            curs.close()
        except ValueError as e:
            print(e)
    
    @property
    def bed_qty(self):
        return self.__bed_qty

    @bed_qty.setter
    def bed_qty(self, qnty):
        try:
            if not isinstance(qnty, int) or qnty <= 0:
                raise ValueError("Bed quantity must be a number and greater than 0")
            self.__bed_qty = qnty
            con = connection
            curs = connection.cursor()

            query = "UPDATE rooms SET bed_qty = %s WHERE id = %s"
            params = (self.__bed_qty, self.__id)

            curs.execute(query, params)
            con.commit()

            curs.close()
        except ValueError as e:
            print(e)

    def add_room(self):
        try:
            con = connection
            curs = connection.cursor()
    
            query = "INSERT INTO rooms(bed_qty, category, type, description, price_per_night) VALUES (%s, %s, %s, %s, %s)"
            params = (self.bed_qty, self.__category.lower(), self.__type.lower(), self.description, self.price_per_night)
            
            curs.execute(query, params)
            con.commit()
    
            curs.close()
        except Exception as e:
            print(f"Error: {e}")


class People:
    def __init__(self, id, f_name, l_name, email):
        self.__id = id
        self._f_name = f_name
        self._l_name = l_name
        self._email = email

    @property
    def id(self):
        return self.__id

    @property
    def f_name(self):
        return self._f_name

    @f_name.setter
    def f_name(self, name, table: str):
        try:
            if len(name) > 16:
                raise ValueError("The first name must have a maximum of 16 characters")
            self._f_name = name
            con = connection
            curs = connection.cursor()

            query = f"UPDATE {table} SET f_name = %s WHERE id = %s"
            params = (self._f_name, self.__id)

            curs.execute(query, params)
            con.commit()

            curs.close()
        except ValueError as e:
            print(e)

    @property
    def l_name(self):
        return self._l_name

    @l_name.setter
    def l_name(self, name, table: str):
        try:
            if len(name) > 16:
                raise ValueError("The last name must have a maximum of 16 characters")
            self._l_name = name
            con = connection
            curs = connection.cursor()
    
            query = f"UPDATE {table} SET l_name = %s WHERE id = %s"
            params = (self._l_name, self.__id)
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
        except ValueError as e:
            print(e)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value, table: str):
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.fullmatch(pattern, value):
                raise ValueError("The Email must have a correct format")
            self._email = value
            con = connection
            curs = connection.cursor()
    
            query = f"UPDATE {table} SET email = %s WHERE id = %s"
            params = (self._email, self.__id)
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
        except ValueError as e:
            print(e)


class Clients(People):
    def __init__(self, id, f_name, l_name, email, nationality, birth_date):
        super().__init__(id, f_name, l_name, email)
        self.nationality = nationality
        self.birth_date = birth_date
        if not id:
            self.add_client()

    def add_client(self):
        try:
            con = connection
            curs = connection.cursor()
    
            query = "INSERT INTO clients(f_name, l_name, email, birth_date, nationality) VALUES (%s, %s, %s, %s, %s)"
            params = (self._f_name, self._l_name, self._email, self.birth_date, self.nationality)
            
            curs.execute(query, params)
            con.commit()

            self._People__id = curs.lastrowid
    
            curs.close()
        except Exception as e:
            print(f"Error: {e}")


class Users(People):
    def __init__(self, id, f_name, l_name, email, password, role):
        super().__init__(id, f_name, l_name, email)
        self.__password = password
        self.role = role

    def add_user(self):
        try:
            con = connection
            curs = connection.cursor()
    
            query = "INSERT INTO users(f_name, l_name, email, password, role) VALUES (%s, %s, %s, %s, %s)"
            params = (self._f_name, self._l_name, self._email, self.__password, self.role)
            
            curs.execute(query, params)
            con.commit()
    
            curs.close()
        except Exception as e:
            print(f"{e}")


class Reservations:
    def __init__(self, id, client_id: int, room_id: int, start_date: datetime, end_date: datetime, status: str, total_price: float = 0.0):
        self.__id = id
        self.start_date = start_date
        self.end_date = end_date
        self.__status = normalize_reservation_status(status)
        self.total_price = total_price
        self.__client_id = client_id
        self.__room_id = room_id

    @property
    def id(self):
        return self.__id
    
    @property
    def room_id(self):
        return self.__room_id

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, status: str):
        normalized = normalize_reservation_status(status)
        try:
            if normalized not in RESERVATION_STATUSES:
                raise ValueError(f"Reservation Status can only be {RESERVATION_STATUSES}, got {status}")
            self.__status = normalized
    
            query = "UPDATE reservations SET status = %s WHERE id = %s"
            params = (self.__status, self.__id)

            con = connection
            curs = connection.cursor()
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
        except ValueError as e:
            print(e)
            
    @property
    def client_id(self):
        return self.__client_id

    def add_reservation(self):
        try:
            con = connection
            curs = connection.cursor()

            query = "INSERT INTO reservations(client_id, room_id, start_date, end_date, status, total_price) VALUES (%s, %s, %s, %s, %s, %s)"
            start_value = self.start_date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(self.start_date, 'strftime') else str(self.start_date)
            end_value = self.end_date.strftime('%Y-%m-%d %H:%M:%S') if hasattr(self.end_date, 'strftime') else str(self.end_date)
            status_value = normalize_reservation_status(self.__status)
            params = (self.__client_id, self.__room_id, start_value, end_value, status_value, self.total_price)
            curs.execute(query, params)
            con.commit()

            self.__id = curs.lastrowid
            inserted_id = self.__id

            curs.close()
            return inserted_id
        except Exception as e:
            print(f"{e}")
            return None

    def update_reservation(self, status: str):
        try:
            con = connection
            curs = connection.cursor()
    
            query = "UPDATE reservations SET status = %s WHERE id = %s AND status = %s"
            params = (status, self.__id, self.__status)
            curs.execute(query, params)
            con.commit()
    
            curs.close()
        except Exception as e:
            print(f"{e}")

    def get_client_name(self):
        try:
            con = connection
            curs = connection.cursor()
    
            query = "SELECT CONCAT(f_name, ' ', l_name) AS full_name FROM clients WHERE clients.id = %s"
            params = (self.__client_id,)
            curs.execute(query, params)
            
            result = curs.fetchone()
            if not result:
                return "Unknown"
            user_full_name = result[0]
            
            curs.close()

            return user_full_name
        except Exception as e:
            print(f"{e}")
            return "Unknown"

    def client_name(self):
        return self.get_client_name()

    def calculate_total(self, season):
        pass