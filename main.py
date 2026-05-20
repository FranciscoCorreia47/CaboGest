from modules.entities import Users, Clients, Reservations, Rooms
from datetime import date, datetime, time, timedelta
import modules.utils as utils

rooms_data = utils.get_all('rooms')
clients_data = utils.get_all('clients')
reservations_data = utils.get_all('reservations')

rooms = list()
clients = list()
reservations = list()

for r in rooms:
  rooms.append(Rooms(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))