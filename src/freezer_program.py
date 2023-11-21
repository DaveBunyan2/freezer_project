from pull_data import pull_data
import time


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

        # Display the last 20 rows of data
        print('Last 20 rows of data:')
        if data is not None:

            # Split the data into lines and filter those starting with "modbusAI"
            lines = data.strip().split('\n')
            filtered_lines = [line.strip()
                              for line in lines if line.startswith('"modbusAI')]

            # Extract and display relevant information from each line
            for line in filtered_lines:
                temp_data = line.split(',')
                print(int(temp_data[5][1]))
        else:
            # Display a message if no data is received
            print('No data received')

        # Display a message indicating the wait time before the next cycle
        print(f'Waiting {wait_time} seconds')

        # Pause execution for the specified wait time
        time.sleep(wait_time)


if __name__ == '__main__':
    data_processor('http://169.254.97.17/getvar.csv', 5)
