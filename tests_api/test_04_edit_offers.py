import pytest
from api.offers import OffersAPI
import copy


class TestEditOffers:

    api = OffersAPI()

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_update_offer_invalid_status(self, auth_user, create_offer_payload, connection_db, create_offer_fixt):
        """Тест редактирования товара с неподходящим статусом"""

        offer_id = create_offer_fixt

        old_description = create_offer_payload["offers"][0]["description"]

        payload = copy.deepcopy(create_offer_payload)
        payload["offers"][0]["description"] = "Новое описание товара для теста"
        payload["offers"][0]["id"] = offer_id

        response = self.api.change_offer(
            headers={"Apitoken": auth_user["api_token"]},
            payload=payload
        )

        response_data = response.json()

        offer_db_description = connection_db.get_offer_by_id(offer_id)

        assert response.status_code == 409, f"Ожидался: 409, получен: {response.status_code}"
        assert "error" in response_data
        assert "message" in response_data
        assert response_data["error"] == "offer_has_invalid_status_for_edit"
        assert response_data["message"] == "Товар в текущем статусе нельзя редактировать"
        assert offer_db_description["description"] == old_description

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("status_id, description", 
                            [
                                (3, "Описание для статуса 3"),
                                (4, "Описание для статуса 4"), 
                                (5, "Описание для статуса 5")
                            ])
    def test_update_offer_valid_status(self, connection_db, create_offer_payload, create_offer_fixt, auth_user, status_id, description):
        """Тест изменение товара в подходящем статусе"""

        offer_id = create_offer_fixt

        connection_db.update_offer_status(status_id, offer_id)

        payload = copy.deepcopy(create_offer_payload)
        payload["offers"][0]["description"] = description
        payload["offers"][0]["id"] = offer_id

        response = self.api.change_offer(
            headers={"Apitoken": auth_user["api_token"]},
            payload=payload
        )

        assert response.status_code == 200

        offer_db_status = connection_db.get_offer_by_id(offer_id)

        assert offer_db_status is not None
        assert offer_db_status["status_id"] == status_id
        assert offer_db_status["description"] == description

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("prop_option, status", 
                                [(9514, 3),
                                (9751, 4), 
                                (9752, 5), 
                                (9753, 4), 
                                (14669, 3)
                                ])
    def test_update_requiered_prop_valid_status(self, connection_db, create_offer_payload, create_offer_fixt, auth_user, prop_option, status):
        """Тест на изменение обязательной характеристики товара в подходящих статусах товара"""

        offer_id = create_offer_fixt

        connection_db.update_offer_status(status, offer_id)

        payload = copy.deepcopy(create_offer_payload)
        payload["offers"][0]["properties"]["149"] = prop_option
        payload["offers"][0]["id"] = offer_id

        response = self.api.change_offer(
            headers={"Apitoken": auth_user["api_token"]},
            payload=payload
        )

        assert response.status_code == 200

        response_data = response.json()

        prop_option_id = connection_db.get_property_option_id(offer_id, 149)["property_option_id"]

        assert prop_option_id is not None
        assert response_data is not None
        assert prop_option_id == prop_option

