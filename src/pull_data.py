import requests


def pull_data(url, requests_module=requests, test=False, verbose=0):
    try:
        response = requests_module.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as err:
        print(f'Error getting data: {err}')
        if test:
            with open('src/getvar.csv', 'r') as file:
                return file.read()
        else:
            return None