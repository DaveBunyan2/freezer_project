from mysql.connector import pooling
from datetime import datetime


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zBZ7j4Ku3QXcF.J',
    'database': 'freezer_db',
}

# Create a connection pool
print('Creating connection pool\n')
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def extract_data(timestamp, id, table):
    # Get connection from pool
    conn = connection_pool.get_connection()

    try:
        if conn.is_connected():
            # Create cursor
            cursor = conn.cursor()

            # Create query
            if table == 'door':
                query = f'''SELECT timestamp, door_status
                           FROM door_sensor_data
                           WHERE timestamp >= STR_TO_DATE("{timestamp}", "%Y-%m-%d") AND sensor_id = {id}'''
            else:
                query = f'''SELECT timestamp, {table}_value
                            FROM {table}_sensor_data
                            WHERE timestamp >= STR_TO_DATE("{timestamp}", "%Y-%m-%d") AND sensor_id = {id}'''
            
            # Execute the query
            cursor.execute(query)

            # Fetch the result
            result = cursor.fetchall()

            return result
    finally:
        cursor.close()
        conn.close()



# Execute the query using the connection pool

result = extract_data('2023-11-28', 1, 'door')

print(result)

