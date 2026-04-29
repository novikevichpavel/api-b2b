import requests

BASE_PATH = "https://api-test6-11.emall.by/api/b2b/v1"

class OfferDraftApi:

    endpoint = "/offer-drafts/bulk"

    def create_offer_draft(self, headers, payload):

         return requests.post(
            f"{BASE_PATH}{self.endpoint}",
            headers=headers,
            json=payload
        )

