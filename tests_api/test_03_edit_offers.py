# import pytest
# from api.offers import OffersAPI
# import copy
# import time


# class TestEditOffers:

#     api = OffersAPI()

#     @pytest.mark.smoke
#     @pytest.mark.regression
#     def test_update_invalid_status(self, auth_user, create_offer_payload, connection_db, create_offer_fixt):
#         """Тест редактирования товара с неподходящим статусом"""

#         offer_id = create_offer_fixt

#         time.sleep(2)

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["description"] = "Новое описание товара для теста"
#         payload["offers"][0]["id"] = offer_id

#         response = self.api.change_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=payload
#         )

#         response_data = response.json()

#         print(response_data)
#         print(response.status_code)

#         assert response.status_code == 409, f"Ожидался: 409, получени: {response.status_code}"
#         assert "error" in response_data
#         assert "message" in response_data
#         assert response_data["error"] == "offer_has_invalid_status_for_edit"
#         assert response_data["message"] == "Товар в текущем статусе нельзя редактировать"