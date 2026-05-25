from modules.db_config import connection, cursor

def get_all(table_name: str):
  curs = cursor

  query = f"SELECT * FROM {table_name}"
  curs.execute(query)

  return curs.fetchall()