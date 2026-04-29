import pytest
import requests
import pymysql
from api.offer_draft import OfferDraftApi
import copy


class TestCreateDraftBulk:

    api = OfferDraftApi()

    def test_create_offer_draft_manually(self, auth_user,):
        """Ручно создание черновика товара с шагом 1"""


    
    
    def test_create_offer_draft_bulk(self, auth_user, create_offer_draft_payload_bulk, connection_db):
        """Проверка создания черновика товара через онлайн-шаблон"""

        response = self.api.create_offer_draft_bulk(
            headers={"Apitoken": auth_user["api_token"]},
            payload=create_offer_draft_payload_bulk
        )

        response_data = response.json()

        print(response_data)

        with connection_db.cursor() as cursor:
            # cursor.execute(
            #     "SELECT seller_id FROM offer_drafts WHERE name = %s;",
            #     (create_offer_draft_payload["offer_drafrs"][0]["name"],)
            # )
            # seller_id_draft_db = cursor.fetchone()

            cursor.execute(
                "SELECT id FROM sellers WHERE unp = %s;", (auth_user["unp"],)
                )
            seller_id_sellers_db = cursor.fetchone()

        print(seller_id_sellers_db["id"])
        # print(seller_id_draft_db["seller_id"])
            


        assert response.status_code == 201, f"Ожидаемый статус - 201. Получен: {response.status_code}"
        assert "message" in response_data, "Не получено сообщение об успешном создании черновика"
        assert response_data["message"] == "Черновики успешно созданы", f"Полученое сообщение отличается от ожидаемого. \
            Получено сообщение {response_data["message"]}"
        assert "created_count" in response_data, "Количество созданных черновиков не получено"
        assert isinstance(response_data["created_count"], int), f"Тип данных каунтера созданных товара отличается от ожидаемого(int). \
            Фактический тип данных: {type(response_data["created_count"])}"
        # assert seller_id_draft_db == seller_id_sellers_db, f"ID из черновка не совпадает с используемым ID. \
        #     ID продавца на черновик {seller_id_draft_db}, ID используемого селлреа {seller_id_sellers_db}"

    # def test_edit_offer_draft(self, auth_user, create_offer_draft_payload)