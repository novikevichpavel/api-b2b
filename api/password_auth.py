import requests

BASE_PATH = "https://api-test6-11.emall.by/api/b2b/v1"

class UserAuth:
    BASE_URL = BASE_PATH

    # def login(self, phone, password):
    #     url = f"{self.BASE_URL}/login/using/password"

    #     payload = {
    #         "phone": phone,
    #         "password": password
    #     }

    #     return requests.post(url, json=payload, verify=False)

    def login(self, payload):
        url = f"{self.BASE_URL}/login/using/password"

        return requests.post(
            url,
            json=payload,
            verify=False
        )