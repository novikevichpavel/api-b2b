import requests
from config.config import API_BASE_URL

class UserAuth:
    BASE_URL = API_BASE_URL

    def login(self, payload):
        url = f"{self.BASE_URL}/login/using/password"

        return requests.post(
            url,
            json=payload,
            verify=False
        )
    
    def sms_login(self, payload):
        url = f"{self.BASE_URL}/login/using/sms"

        return requests.post(
            url,
            json=payload,
            verify=False
        )
        
