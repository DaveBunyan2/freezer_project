def extract_data(start_date, end_date, id, table, connection_pool):
    try:
        conn = connection_pool.get_connection()

        cursor = conn.cursor()

        # Create query
        if table == 'door':
            query = f'''SELECT timestamp, door_status
                        FROM door_sensor_data
                        WHERE timestamp BETWEEN STR_TO_DATE("{start_date}", "%Y-%m-%d") AND STR_TO_DATE("{end_date}", "%Y-%m-%d") 
                        AND sensor_id = {id}'''
        else:
            query = f'''SELECT timestamp, {table}_value
                        FROM {table}_sensor_data
                        WHERE timestamp BETWEEN STR_TO_DATE("{start_date}", "%Y-%m-%d") AND STR_TO_DATE("{end_date}", "%Y-%m-%d") 
                        AND sensor_id = {id}'''
            
        # Execute the query
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchall()

        return result
    
    except Exception as err:
        print(f'Error: {err}')

    finally:
        cursor.close()
        conn.close()

def extract_last(id, table, connection_pool):
    try:
        conn = connection_pool.get_connection()

        cursor = conn.cursor()

        query = f'''SELECT {table}_value
                    FROM {table}_sensor_data
                    WHERE sensor_id = {id}
                    ORDER BY timestamp DESC
                    LIMIT 1'''

        cursor.execute(query)

        result = cursor.fetchall()

        return result

    except Exception as err:
        print(f'Error: {err}')
    
    finally:
        cursor.close()
        conn.close()