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

        assert response.status_code == 409, f"Ожидался: 409, получени: {response.status_code}"
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

        with connection_db.cursor() as cursor:
            cursor.execute("UPDATE offers SET status_id = %s WHERE id = %s", (status_id, offer_id))
            connection_db.commit()

        payload = copy.deepcopy(create_offer_payload)
        payload["offers"][0]["description"] = description
        payload["offers"][0]["id"] = offer_id

        response = self.api.change_offer(
            headers={"Apitoken": auth_user["api_token"]},
            payload=payload
        )

        with connection_db.cursor() as cursor:
            cursor.execute("SELECT status_id, description FROM offers WHERE id = %s", (offer_id,))
            db_data = cursor.fetchone()

        assert response.status_code == 204
        assert db_data is not None
        assert db_data["status_id"] == status_id
        assert db_data["description"] == description

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("prop_option", [9514, 9751, 9752, 9753, 14669])
    def test_update_requiered_prop_valid_status(self, connection_db, create_offer_payload, create_offer_fixt, auth_user, prop_option):

        offer_id = create_offer_fixt

        with connection_db.cursor() as cursor:
            cursor.execute("UPDATE offers SET status_id = 3 WHERE id = %s", (offer_id,))
            connection_db.commit()

        payload = copy.deepcopy(create_offer_payload)
        payload["offers"][0]["properties"]["149"] = prop_option
        payload["offers"][0]["id"] = offer_id

        response = self.api.change_offer(
            headers={"Apitoken": auth_user["api_token"]},
            payload=payload
        )

        response_data = response.json()

        with connection_db.cursor() as cursor:
            cursor.execute("SELECT id FROM offer_properties WHERE offer_id = %s AND property_id = %s", (offer_id, 149))
            offer_prop_id = cursor.fetchone()["id"]

            cursor.execute("SELECT property_option_id FROM offer_property_values WHERE offer_property_id = %s", (offer_prop_id,))
            prop_option_id = cursor.fetchone()["property_option_id"]

        assert prop_option_id is not None

        assert response_data is not None
        assert response.status_code == 200
        assert prop_option_id == prop_option

