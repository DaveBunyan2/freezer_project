from datetime import datetime


def extract_data(timestamp, id, table, connection_pool):
    try:
        conn = connection_pool.get_connection()

        cursor = conn.cursor()

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
    
    except Exception as err:
        print(f'Error: {err}')

    finally:
        cursor.close()
        conn.close()