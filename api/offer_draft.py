import requests
from config.config import API_BASE_URL


class OfferDraftApi:
    BASE_URL = API_BASE_URL

    endpoint = "/offer-drafts"
    bulk_endpoint = "/offer-drafts/bulk"

    def create_offer_draft_manually(self, headers, payload):
         
        return requests.post(
            f"{self.BASE_URL}{self.endpoint}",
            headers=headers,
            json=payload
        )

    def create_offer_draft_bulk(self, headers, payload):

         return requests.post(
            f"{self.BASE_URL}{self.bulk_endpoint}",
            headers=headers,
            json=payload
        )

    # def edit_offer_draft