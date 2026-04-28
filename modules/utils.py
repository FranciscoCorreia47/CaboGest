from db_config import connection, cursor

def get_all(table_name: str):
  curs = cursor

  query = "SELECT * FROM %(table_name)s"
  curs.execute(query, {'table_name': table_name})

  return curs.fetchall()