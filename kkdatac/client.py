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

    def create_factor(self, name: str, description: str, category: str, code: str, 
                     metadata: dict = None, is_public: bool = False) -> dict:
        """Create a new factor"""
        url = f"{self.base_url}/api/v1/factors/"
        payload = {
            "name": name,
            "description": description,
            "category": category,
            "code": code,
            "metadata": metadata or {},
            "is_public": is_public
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to create factor: {response.status_code} - {response.text}")

    def list_factors(self, category: str = None) -> list:
        """List available factors"""
        url = f"{self.base_url}/api/v1/factors/"
        if category:
            url += f"?category={category}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to list factors: {response.status_code} - {response.text}")

    def get_factor(self, factor_id: int) -> dict:
        """Get factor details"""
        url = f"{self.base_url}/api/v1/factors/{factor_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to get factor: {response.status_code} - {response.text}")

    def evaluate_factor(self, factor_id: int, returns_data: pd.DataFrame) -> dict:
        """Evaluate factor performance"""
        url = f"{self.base_url}/api/v1/factors/{factor_id}/evaluate"
        response = requests.post(url, json={"returns_data": returns_data.to_dict()}, 
                               headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to evaluate factor: {response.status_code} - {response.text}")

    def get_factor_data(
        self,
        order_book_ids: str | list[str],
        factors: str | list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        universe: str | None = None,
        expect_df: bool = True
    ) -> pd.DataFrame:
        """Get factor data from server"""
        url = f"{self.base_url}/api/v1/factors/data"
        params = {
            "order_book_ids": order_book_ids if isinstance(order_book_ids, str) else ",".join(order_book_ids),
            "factors": factors if isinstance(factors, str) else ",".join(factors) if factors else None,
            "start_date": start_date,
            "end_date": end_date,
            "universe": universe,
            "expect_df": expect_df
        }
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return pd.DataFrame(result["data"]) if expect_df else result["data"]
        raise Exception(f"Failed to get factor data: {response.status_code} - {response.text}")

    def get_factor_exposure(
        self,
        order_book_ids: str | list[str],
        start_date: str,
        end_date: str,
        factors: str | list[str] | None = None,
        industry_mapping: str = 'sws_2021'
    ) -> pd.DataFrame:
        """Get factor exposure data"""
        url = f"{self.base_url}/api/v1/factors/exposure"
        params = {
            "order_book_ids": order_book_ids if isinstance(order_book_ids, str) else ",".join(order_book_ids),
            "start_date": start_date,
            "end_date": end_date,
            "factors": factors if isinstance(factors, str) else ",".join(factors) if factors else None,
            "industry_mapping": industry_mapping
        }
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return pd.DataFrame(result["data"])
        raise Exception(f"Failed to get factor exposure: {response.status_code} - {response.text}")

    def get_factor_return(
        self,
        start_date: str,
        end_date: str,
        factors: str | list[str] | None = None,
        universe: str = 'whole_market',
        method: str = 'implicit',
        industry_mapping: str = 'sws_2021'
    ) -> pd.DataFrame:
        """Get factor returns"""
        url = f"{self.base_url}/api/v1/factors/return"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "factors": factors if isinstance(factors, str) else ",".join(factors) if factors else None,
            "universe": universe,
            "method": method,
            "industry_mapping": industry_mapping
        }
        response = requests.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            return pd.DataFrame(result["data"])
        raise Exception(f"Failed to get factor returns: {response.status_code} - {response.text}")


# Example usage:
if __name__ == "__main__":
    client = KKDataClient()

    # Run a query and get a pandas DataFrame
    query = "show databases"
    df = client.run_query(query)
    print(df)
