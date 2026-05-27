from modules.db_config import connection, cursor

def get_all(table_name: str):
  curs = cursor

  query = f"SELECT * FROM {table_name}"
  curs.execute(query)

  return curs.fetchall()

def get_clientId_by_email(email: str):
  curs = cursor

  query = "SELECT id FROM users WHERE email = %s"
  curs.execute(query, email)

  data = curs.fetchall()

  id = 0

  for d in data:
    id = d

  return id