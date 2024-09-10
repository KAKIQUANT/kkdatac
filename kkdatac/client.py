import requests
import pandas as pd
import lz4.frame
import binascii
import pickle
import warnings
from kkdatac.config import KKDATAD_ENDPOINT

class KKDataClient:
    def __init__(self, base_url: str = KKDATAD_ENDPOINT, api_key: str | None = None):
        """
        Initialize the client with the base URL of the kkdatad server and an API key.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {'api_key': self.api_key}

    def _decompress_data(self, compressed_data_hex: str):
        """
        Decompress the received hex-encoded LZ4 compressed data.
        Also returns the size of the compressed and decompressed data.
        """
        import time
        start = time.time()
        # Convert hex to binary
        compressed_data = binascii.unhexlify(compressed_data_hex)
        conversion_time = time.time() - start
        # Size of the compressed data
        compressed_size = len(compressed_data)

        # Decompress data
        decompressed_data = lz4.frame.decompress(compressed_data)
        decompression_time = time.time() - start - conversion_time
        # Size of the decompressed data
        decompressed_size = len(decompressed_data)

        # Load the decompressed pickle data into Python objects
        data = pickle.loads(decompressed_data)
        data_load_time = time.time() - start - conversion_time - decompression_time
        print(f"Traffic used: {compressed_size} bytes (compressed), {decompressed_size} bytes (decompressed)")
        print(f"Time used: {conversion_time:.2f} s (conversion), {decompression_time:.2f} s (decompression), {data_load_time:.2f} s (loading)")
        return data

    def run_query(self, sql_query: str) -> pd.DataFrame:
        """
        Send a SQL query to the kkdatad server and return the result as a pandas DataFrame.
        """
        if self.api_key is None:
            warnings.warn("API key is not set. Using free version now. Some features may not be available.")
            # Free version: append the query to the URL
            url = f"{self.base_url}/sql-free/?query={requests.utils.quote(sql_query)}"
            response = requests.post(url)
        else:
            # Non-free version: append the query to the URL
            url = f"{self.base_url}/sql/?query={requests.utils.quote(sql_query)}"
            # Correct the header to match your curl command
            headers = {'api-key': self.api_key, 'accept': 'application/json'}
            # Send the request with API key in headers
            response = requests.post(url, headers=headers)

        # Handle the response
        if response.status_code == 200:
            result = response.json()
            compressed_data_hex = result['data']
            return self._decompress_data(compressed_data_hex)
        else:
            raise Exception(f"Failed to query data: {response.status_code} - {response.text}")

    @staticmethod
    def get_apikey(username: str, password: str) -> str:
        """
        Get an API key from the kkdatad server using a username and password.
        """
        url = f"{KKDATAD_ENDPOINT}/login/"
        payload = {'username': username, 'password': password}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['access_token']
        else:
            raise Exception(f"Failed to get API key: {response.status_code} - {response.text}")

    @staticmethod
    def register(username: str, password: str) -> str:
        """
        Register a new user on the kkdatad server.
        """
        url = f"{KKDATAD_ENDPOINT}/register/"
        payload = {'username': username, 'password': password}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['message']
        else:
            raise Exception(f"Failed to register user: {response.status_code} - {response.text}")


# Example usage:
if __name__ == "__main__":
    client = KKDataClient()

    # Run a query and get a pandas DataFrame
    query = "show databases"
    df = client.run_query(query)
    print(df)
