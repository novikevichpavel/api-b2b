import pytest
import requests
import pymysql
from api.password_auth import UserAuth
import copy


class TestSellerAuth:

    api = UserAuth()

    def test_user_auth(self, auth_user_payload):
        """Тест авторизации с валидными данными"""

        response = self.api.login(
            auth_user_payload
        )

        response_data = response.json()

        print(response_data)

        assert response.status_code == 200, f"Ожидаемый статус - 200 ОК. Получен - {response.status_code}"

    def test_ivalid_phone_number(self, auth_user_payload):
        """Тест валидации невалидного номера телефона"""

        payload = copy.deepcopy(auth_user_payload)
        payload["phone"] = "+375293397268"

        response = self.api.login(
            payload
        )

        response_data = response.json()
        print(response_data)

        assert response.status_code == 422, f"Ожидаемый статус код - 422. Получен: {response.status_code}"
        assert "errors" in response_data, "Валидационное сообщение отсутсвует в теле ответа"
        assert "phone" in response_data["errors"], "Отсутсвует указание на поле с ошибкой в теле ответа"
        assert response_data["errors"]["phone"][0] == "Введенный номер телефона не связан ни с одним УНП", \
            "Валидацинное сообщение не соответсвует ожидаемому"
    
    def test_ivalid_password(self, auth_user_payload):
        """Тест валидации невалидного пароля"""
        
        payload = copy.deepcopy(auth_user_payload)
        payload["password"] = "123456789"

        response = self.api.login(
            payload
        )

        response_data = response.json()

        print(response_data.get("message"))

        assert response.status_code == 404, f"Ожидаемый статус - 404. Получен {response.status_code}"
        assert response_data.get("message")  == "Неверный номер телефона или пароль"

    def test_response_token(self, auth_user_payload):
        """Тест на наличие авторизационного токена в ответе от сервера"""
        
        response = self.api.login(
            auth_user_payload
        )

        response_data = response.json()

        print(response_data.get('api_token'))

        assert "api_token" in response_data, f"Токен отсутствует в ответе"
        
    def test_get_unp_in_response(self, auth_user_payload):
        """Тест наличия унп в ответе от сервера"""
        
        response = self.api.login(
            auth_user_payload
        )

        response_data = response.json()
        print(f"УНП продавца: {response_data.get('unp')}")

        assert "unp" in response_data, f"unp не получен"

    def test_check_response_unp_with_db(self, connection_db, auth_user_payload):
        """Тест на совпадения унп из ответа с унп в БД"""

        response = self.api.login(
            auth_user_payload
        )

        response_data = response.json()
        seller_unp = response_data.get("unp")

        with connection_db.cursor() as cursor:
            cursor.execute("SELECT unp FROM seller_accounts WHERE unp = %s;", (seller_unp,))
            db_unp = cursor.fetchone()

        print(f"Получен УНП: {db_unp["unp"]}")

        assert db_unp is not None, "UNP не найден в БД"
        assert db_unp["unp"] == seller_unp

    def test_check_reposnse_token_with_db(self, connection_db, auth_user_payload):
        """Тест на совпадения токена из ответа с токеном, записанным в БД"""
        
        response = self.api.login(
            auth_user_payload
        )

        response_data = response.json()

        seller_unp = response_data.get("unp")

        phone_num = auth_user_payload["phone"]

        with connection_db.cursor() as cursor:
            cursor.execute("SELECT api_token FROM seller_accounts WHERE unp = %s AND phone = %s", (seller_unp, phone_num))
            db_token = cursor.fetchone()

        print(f"Получен токнен БД: {db_token["api_token"]}")

        assert response_data.get("api_token") == db_token["api_token"], "Токен не совпадает"

    def test_empty_password_auth(self, auth_user_payload):
        """Тест валидации при авторизации без передачи пароля"""

        payload = copy.deepcopy(auth_user_payload)
        payload["password"] = ""

        response = self.api.login(
            payload
        )

        response_data = response.json()

        print(response_data)

        assert response.status_code == 422, f"Ожидаемый статус - 422. Получен {response.status_code}"
        assert "errors" in response_data, "Отсутствует валидационное сообщение в ответе от сервера"
        assert "password" in response_data["errors"], "Отсутствует указание на поле с ошибкой в ответе от сервера"
        assert response_data["errors"]["password"][0] == "Обязательное поле", f"Текст ошибки отличается от ожидаемого. \
            Получен {response_data["errors"]["password"][0]}"

    def test_empty_phone_auth(self, auth_user_payload):
        """"""

        payload = copy.deepcopy(auth_user_payload)
        payload["phone"] = ""

        response = self.api.login(
            payload
        )

        response_data = response.json()

        print(response_data)

        assert response.status_code == 422, f"Ожидаемый статус - 422. Получен: {response.status_code}"
        assert "errors" in response_data, "Отсутствует валдиацинное сообщение в ответе от сервера"
        assert "phone" in response_data["errors"], "Отсутствует указание на поле с ошибкой в ответе от сервера"
        assert response_data["errors"]["phone"][0] == "Обязательное поле", f"Текст ошибки отличается от ожидаемого. \
            Получен {response_data["errors"]["phone"][0]}"