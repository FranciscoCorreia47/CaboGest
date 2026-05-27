from modules.db_config import connection, cursor
from datetime import date, time, datetime, timedelta
import re

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
            else:
                self.__category = value
            con = connection
            curs = cursor
    
            query = "UPDATE rooms SET category = %s WHERE id = %d"
            params = (self.category(), self.id())
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except ValueError as e:
            print(e)

    @property
    def type(self):
        return self.__category

    @type.setter
    def type(self, value):
        try:
            if value not in ["Suite", "Single"]:
                raise ValueError(f"Room Type can only be 'Suite' or 'Single', got {value}")
            else:
                self.__type = value
            con = connection
            curs = cursor
    
            query = "UPDATE rooms SET type = %s WHERE id = %d"
            params = (self.type(), self.id())
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except ValueError as e:
            print(e)

    @property
    def occupied(self):
        return self.__occupied
    
    @occupied.setter
    def update_status(self, status: int):
        try:
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
        except ValueError as e:
            print(e)
    
    @property
    def bed_qty(self):
        return self.__bed_qty

    @bed_qty.setter
    def bed_qty(self, qnty):
        try:
            if not (qnty.isdigit()) or qnty <= 0:
                raise ValueError(f"Bed quantity must be a number and greater than 0")
            else:
                self.__bed_qty = qnty
            con = connection
            curs = cursor
    
            query = "UPDATE rooms SET bed_qty = %d WHERE id = %d"
            params = (self.bed_qty(), self.id())
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except ValueError as e:
            print(e)

    def add_room(self):
        try:
            con = connection
            curs = cursor
    
            query = "INSERT INTO rooms(bed_qty, category, type, description, price_per_night) VALUES (%d, %s, %s, %s, %f)"
            params = (self.bed_qty, self.category, self.type, self.description, self.price_per_night)
            
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
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
                raise ValueError(f"The first name must have a maximum of 16 characters")
            else:
                self._f_name = name
            con = connection
            curs = cursor
    
            query = f"UPDATE {table} SET f_name = %s WHERE id = %d"
            params = (self._f_name(), self.id())
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except ValueError as e:
            print(e)

    @property
    def l_name(self):
        return self._f_name

    @l_name.setter
    def l_name(self, name, table: str):
        try:
            if len(name) > 16:
                raise ValueError(f"The last name must have a maximum of 16 characters")
            else:
                self._l_name = name
            con = connection
            curs = cursor
    
            query = f"UPDATE {table} SET l_name = %s WHERE id = %d"
            params = (self._l_name(), self.id())
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except ValueError as e:
            print(e)

    @property
    def email(self):
        return self._f_name

    @email.setter
    def email(self, value, table: str):
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.fullmatch(pattern, value) == False:
                raise ValueError(f"The Email must have a correct format")
            else:
                self._email = value
            con = connection
            curs = cursor
    
            query = f"UPDATE {table} SET email = %s WHERE id = %d"
            params = (self._email(), self.id())
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except ValueError as e:
            print(e)


class Clients(People):
    def __init__(self, id, f_name, l_name, email, nationality, birth_date):
        super().__init__(id, f_name, l_name, email)
        self.nationality = nationality
        self.birth_date = birth_date
        self.add_client()

    def add_client(self):
        try:
            con = connection
            curs = cursor
    
            query = "INSERT INTO clients(f_name, l_name, email, birth_date, nationality) VALUES (%s, %s, %s, %s, %s)"
            params = (self._f_name, self._l_name, self._email, self.birth_date, self.nationality)
            
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
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
            curs = cursor
    
            query = "INSERT INTO users(f_name, l_name, email, password, role) VALUES (%s, %s, %s, %s, %s)"
            params = (self._f_name, self._l_name, self._email, self.__password, self.role)
            
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except Exception as e:
            print(f"{e}")


class Reservations:
    def __init__(self, id, client_id: int, room_id: int, start_date: datetime, end_date: datetime, status: str, total_price: float = 0.0):
        self.__id = id
        self.start_date = start_date
        self.end_date = end_date
        self.__status = status
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
        try:
            if status not in ["Checked In", "Checked Out", "Transfered", "Canceled"]:
                raise ValueError(f"Reservation Status can only be 'Checked In', 'Checked Out', 'Transfered' or 'Canceled', got {status}")
            else:
                self.__status = status
            con = connection
            curs = cursor
    
            query = "UPDATE reservations SET status = %s WHERE id = %d"
            params = (self.status(), self.id())
    
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except ValueError as e:
            print(e)
            
    def add_reservation(self):
        try:
            con = connection
            curs = cursor
    
            query = "INSERT INTO reservations(client_id, room_id, start_date, end_date) VALUES (%d, %d, %s, %s)"
            params = (self.__client_id, self.__room_id, self.start_date.strftime('%Y-%m-%d %H:%M:%S'), self.end_date.strftime('%Y-%m-%d %H:%M:%S'))
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except Exception as e:
            print(f"{e}")

    def update_reservation(self, status: str):
        try:
            con = connection
            curs = cursor
    
            query = "UPDATE reservations SET status = %s WHERE id = %d AND status = %s"
            params = (status, self.id(), self.status)
            curs.execute(query, params)
            con.commit()
    
            curs.close()
            con.close()
        except Exception as e:
            print(f"{e}")

    def get_client_name(self):
        try:
            con = connection
            curs = cursor
    
            query = "SELECT CONCAT(f_name, ' ', l_name) AS full_name FROM clients WHERE clients.id = %d"
            params = (self.__client_id)
            curs.execute(query, params)
            con.commit()
            
            result = curs.fetchall()
            user_full_name = result[0][0]
            
            curs.close()
            con.close()

            return user_full_name
        except Exception as e:
            print(f"{e}")
    
    def calculate_total(season):
        pass