import requests
import time


def pull_data(url, requests_module=requests, test=False, verbose=0):
    """
    Fetch data from a specified URL using the requests library.

    Parameters:
    - url (str): The URL to fetch data from.
    - requests_module (module): The requests module or a mock module for testing purposes.
                              Defaults to the requests module.
    - test (bool): If True, the function returns sample data from a local file if the request fails.
                   Defaults to False.
    - verbose (int): Controls the verbosity of output. Higher values result in more verbose output.
                    Defaults to 0.

    Returns:
    - str or None: The fetched data as text if successful, or None if there's an error (and not in test mode).

    Raises:
    - requests.RequestException: If an error occurs while making the HTTP request.
    """
    tic = time.time()
    try:
        # Make an HTTP GET request to the specified URL
        if verbose >= 1:
            print(f'Making GET request to {url}')
        response = requests_module.get(url)

        # Check for HTTP status code errors
        response.raise_for_status()
        toc = time.time()
        if verbose >= 1:
            print(
                f'Request finished with status code {response.status_code}\nReturning data')
        if verbose >= 2:
            print(f'Time taken for get request: {toc - tic}')
        # Return the text content of the response
        return response.text, toc - tic

    except requests.RequestException as err:
        # Print error message
        if verbose >= 2:
            toc = time.time()
            print(
                f'Error getting data: {err}\nTime taken to fail: {toc - tic}')
        elif verbose >= 1:
            print('Error getting data')

        # If in test mode, return sample data from a local file
        if test:
            toc = time.time()
            if verbose >= 1:
                print('Using test data')
            if verbose >= 2:
                print(f'Time taken for request: {toc - tic}')
            with open('src/getvar.csv', 'r') as file:
                return file.read(), toc - tic

        # If not in test mode, return None
        else:
            toc = time.time()
            if verbose >= 2:
                print('Returning')
                print(f'Time taken since requesting data: {toc - tic}')
            return None, toc - tic
