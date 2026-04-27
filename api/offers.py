import requests

BASE_PATH = "https://api-test6-11.emall.by/api/b2b/v1"


class OffersAPI:

    endpoint = "/offers"

    def create_offer(self, headers, payload):

        return requests.post(
            f"{BASE_PATH}{self.endpoint}",
            headers=headers,
            json=payload
        )
    
    def change_offer(self, headers, payload):

        return requests.put(
            f"{BASE_PATH}{self.endpoint}",
            headers=headers,
            json=payload
        )