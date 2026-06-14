from modules.db_config import connection

def get_all(table_name: str):
  curs = connection.cursor()
  try:
    query = f"SELECT * FROM {table_name}"
    curs.execute(query)
    return curs.fetchall()
  finally:
    curs.close()

def get_client_id_by_email(email: str):
  curs = connection.cursor()
  try:
    query = "SELECT id FROM clients WHERE LOWER(email) = LOWER(%s)"
    curs.execute(query, (email,))

    data = curs.fetchone()
    if not data:
      return None
    return data[0]
  finally:
    curs.close()