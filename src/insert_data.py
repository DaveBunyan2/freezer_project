import mysql.connector


def insert_data(data, connection_pool, table_name):
    '''
    Insert data into a specified table using a connection pool.

    Parameters:
    - data (list): A list of tuples containing the data to be inserted. Each tuple should correspond to a row.
    - connection_pool (mysql.connector.MySQLConnectionPool): A connection pool to acquire database connections.
    - table_name (str): The name of the table where the data will be inserted.

    Returns:
    None

    Raises:
    - Exception: Any exception raised during the database interaction will be caught, and the function will print an error message.

    Usage:
    - Example: insert_data([(timestamp1, sensor_id1, value1), (timestamp2, sensor_id2, value2)], your_connection_pool, 'your_table_name')
    '''
    try:
        # Acquire a connection from the pool
        conn = connection_pool.get_connection()

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Define SQL query for data insertion
        query = f'''INSERT INTO {table_name} (timestamp, sensor_id, value) 
                   VALUES (%s, %s, %s)'''

        # Insert data into the table
        cursor.executemany(query, data)

        # Commit the changes
        conn.commit()

    except Exception as err:
        # Rollback in case of an error
        print(f"Error: {err}")
        conn.rollback()

    finally:
        # Close the cursor
        cursor.close()

        # Release the connection back to the pool
        connection_pool.release_connection(conn)
