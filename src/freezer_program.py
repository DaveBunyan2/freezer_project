#!/usr/bin/env python3
from pull_data import pull_data
from insert_data import insert_data
import time
from datetime import datetime
import mysql.connector
from mysql.connector import pooling


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zBZ7j4Ku3QXcF.J',
    'database': 'freezer_db',
}

# Create a connection pool
print('Creating connection pool')
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)


# Dictionary mapping analog input to amp and temperature sensor ID
analog_mapping = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '6': 1,
    '7': 2,
    '8': 3,
    '9': 4,
    '10': 5,
    '11': 6,
    '12': 7,
    '13': 8
}

# Dictionary mapping binary input to water level and door sensor ID
binary_mapping = {
    '1': 1,
    '2': 2,
    '3': 1
}

# List of amp sensor IDs
amp_ids = ['1', '2', '3', '4']

# List of temperature sensor IDs
temperature_ids = ['6', '7', '8', '9', '10', '11', '12', '13']

# List of water level sensor IDs
water_ids = ['1', '2']

# List of door sensor IDs
door_ids = ['3']


def get_id(id_string):
    """
    Extracts numeric characters from a given string and returns them as a single string.

    Parameters:
    - id_string (str): The input string from which numeric characters will be extracted.

    Returns:
    - str: A string containing only the numeric characters found in the input string.
    """
    # Initialize an empty string to store numeric characters
    id_result = ''

    # Iterate through each character in the input string
    for character in id_string:
        # Check if the character is numeric
        if character.isnumeric():
            # Append the numeric character to the result string
            id_result += character

    # Return the final string containing numeric characters
    return id_result


def data_processor(url, wait_time):
    """
    Continuously fetches and processes data from a specified URL.

    Parameters:
    - url (str): The URL to fetch data from.
    - wait_time (int): The time to wait (in seconds) between each data fetch and processing cycle.

    Returns:
    - None: The function runs indefinitely and doesn't return a value.
    """
    while True:

        # Display a message indicating data retrieval is in progress
        print('Getting data')

        # Fetch data using the pull_data function (test mode)
        data = pull_data(url, test=True)

        # Get timestamp
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        if data is not None:
            print('Extracting relevant data')
            temperature_data = []
            amp_data = []
            water_data = []
            door_data = []

            # Split the data into lines and filter those starting with "modbusAI
            lines = data.strip().split('\n')
            filtered_AI_lines = [line.strip()
                              for line in lines if line.startswith('"modbusAI')]

            # Extract and store data in database
            for line in filtered_AI_lines:
                # Split data at commas
                temp_AI_data = line.split(',')

                # Get ID of input
                id = get_id(temp_AI_data[0])

                if id in amp_ids:
                    amp_data.append(
                        (timestamp, analog_mapping[id], int(temp_AI_data[5][1: -1])))
                elif id in temperature_ids:
                    temperature_data.append(
                        (timestamp, analog_mapping[id], int(temp_AI_data[5][1: -1])))
            # Sort data by temperature ID
            temperature_data.sort(key=lambda x: x[1])

            insert_data(temperature_data, connection_pool, 'temperature')
            insert_data(amp_data, connection_pool, 'amp')

            # Split the data into lines and filter those starting with "modbusDI
            filtered_DI_lines = [line.strip() for line in lines if line.startswith('"modbusDI')]

            # Extract and store data in database
            for line in filtered_DI_lines:
                # Split data at commas
                temp_DI_data = line.split(',')

                # Get ID of input
                id = get_id(temp_DI_data[0])

                if id in water_ids:
                    water_data.append((timestamp, binary_mapping[id], int(temp_DI_data[5][1: -1])))
                elif id in door_ids:
                    door_data.append((timestamp, binary_mapping[id], int(temp_DI_data[5][1: -1])))

            insert_data(water_data, connection_pool, 'water_level')
            insert_data(door_data, connection_pool, 'door')
        else:
            # Display a message if no data is received
            print('No data received')

        # Display a message indicating the wait time before the next cycle
        print(f'Waiting {wait_time} seconds')

        # Pause execution for the specified wait time
        time.sleep(wait_time)


if __name__ == '__main__':
    data_processor('http://169.254.97.17/getvar.csv', 5)
