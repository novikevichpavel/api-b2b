import pytest
import requests
import pymysql
from api.offer_draft import OfferDraftApi
import copy
import time


class TestCreateDraft:

    api = OfferDraftApi()

    def test_create_offer_draft_manually(self, auth_user, create_offer_draft_manually_payload_first):
        """Одиночное создание черновика товара шаг 1"""

        response = self.api.create_offer_draft_manually(
            headers={"Apitoken": auth_user["api_token"]},
            payload=create_offer_draft_manually_payload_first
        )

        response_data = response.json()

        print(response_data)

        assert response.status_code == 201
        assert "message" in response_data
        assert response_data["message"] == "Товар сохранен как черновик"

    def test_create_draft_manually(self, auth_user, create_offer_draft_manually_payload_first, connection_db, get_seller_id_from_db):
        """Одиночное создание черновика товара шаг 2, но без заполненения характеристик для второго шага"""

        payload = copy.deepcopy(create_offer_draft_manually_payload_first)
        payload["step"] = 2
        payload["curStep"] = 2

        response = self.api.create_offer_draft_manually(
            headers={"Apitoken": auth_user["api_token"]},
            payload=payload
        )

        response_data = response.json()

        print(response_data)

        seller_id = get_seller_id_from_db

        with connection_db.cursor() as cursor:
            # cursor.execute("SELECT id FROM seller")

            cursor.execute(
                "SELECT * FROM offers WHERE seller_id = %s;",
                (seller_id,)
            )

            db_data = cursor.fetchall()
        
        print(db_data)

        assert response.status_code == 201
        assert "message" in response_data
        assert response_data["message"] == "Товар сохранен как черновик"

    # def test_create_offer_draft_manually(self, auth_user, create_offer_draft_manually_payload_third):
    #     """Одиночное создание черновика товара с шагом 3"""

    #     response = self.api.create_offer_draft_manually(
    #         headers={"Apitoken": auth_user["api_token"]},
    #         payload=create_offer_draft_manually_payload_third
    #     )
    
    #     response_data = response.json()

    #     print(response_data)

    #     assert response.status_code == 201, f"Ожидаемый статус - 201. Получен: {response.status_code}"
    #     assert "message" in response_data, f""
    #     assert response_data["message"] == "Товар сохранен как черновик"
    
    # def test_create_offer_draft_bulk(self, auth_user, create_offer_draft_bulk_payload, connection_db):
    #     """Проверка создания черновика товара через онлайн-шаблон"""

    #     response = self.api.create_offer_draft_bulk(
    #         headers={"Apitoken": auth_user["api_token"]},
    #         payload=create_offer_draft_bulk_payload
    #     )

    #     response_data = response.json()

    #     print(response_data)

    #     with connection_db.cursor() as cursor:
    #         # cursor.execute(
    #         #     "SELECT seller_id FROM offer_drafts WHERE name = %s;",
    #         #     (create_offer_draft_payload["offer_drafrs"][0]["name"],)
    #         # )
    #         # seller_id_draft_db = cursor.fetchone()

    #         cursor.execute(
    #             "SELECT id FROM sellers WHERE unp = %s;", (auth_user["unp"],)
    #             )
    #         seller_id_sellers_db = cursor.fetchone()

    #     print(seller_id_sellers_db["id"])
    #     # print(seller_id_draft_db["seller_id"])
            


    #     assert response.status_code == 201, f"Ожидаемый статус - 201. Получен: {response.status_code}"
    #     assert "message" in response_data, "Не получено сообщение об успешном создании черновика"
    #     assert response_data["message"] == "Черновики успешно созданы", f"Полученое сообщение отличается от ожидаемого. \
    #         Получено сообщение {response_data["message"]}"
    #     assert "created_count" in response_data, "Количество созданных черновиков не получено"
    #     assert isinstance(response_data["created_count"], int), f"Тип данных каунтера созданных товара отличается от ожидаемого(int). \
    #         Фактический тип данных: {type(response_data["created_count"])}"
    #     # assert seller_id_draft_db == seller_id_sellers_db, f"ID из черновка не совпадает с используемым ID. \
    #     #     ID продавца на черновик {seller_id_draft_db}, ID используемого селлреа {seller_id_sellers_db}"

    # # def test_edit_offer_draft(self, auth_user, create_offer_draft_payload)