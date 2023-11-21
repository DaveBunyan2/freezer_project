import requests


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
    try:
        # Make an HTTP GET request to the specified URL
        response = requests_module.get(url)

        # Check for HTTP status code errors
        response.raise_for_status()

        # Return the text content of the response
        return response.text

    except requests.RequestException as err:
        # Print error message
        print(f'Error getting data: {err}')

        # If in test mode, return sample data from a local file
        if test:
            with open('src/getvar.csv', 'r') as file:
                return file.read()

        # If not in test mode, return None
        else:
            return None
