from pull_data import pull_data
import time


def data_processor(url, wait_time):
    while True:
        print('Getting data')
        data = pull_data(url, test=True)
        print('Last 20 rows of data:')
        if data is not None:
            lines = data.strip().split('\n')

            # Filter lines that start with "modbusAI"
            filtered_lines = [line.strip() for line in lines if line.startswith('"modbusAI')]

            # Print the filtered lines
            for line in filtered_lines:
                temp_data = line.split(',')
                print(temp_data[5])
        else:
            print('No data received')
        print(f'Waiting {wait_time} seconds')
        time.sleep(wait_time)

if __name__ == '__main__':
    data_processor('http://169.254.97.17/getvar.csv', 5)
