import requests
from config.config import API_BASE_URL


class OffersAPI:
    BASE_URL = API_BASE_URL

    endpoint = "/offers"

    def create_offer(self, headers, payload):

        return requests.post(
            f"{self.BASE_URL}{self.endpoint}",
            headers=headers,
            json=payload
        )
    
    def change_offer(self, headers, payload):

        return requests.put(
            f"{self.BASE_URL}{self.endpoint}",
            headers=headers,
            json=payload
        )