import pytest
from api.password_auth import UserAuth
import copy


class TestSellerAuth:

    api = UserAuth()

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_user_auth(self, auth_user_payload):
        """Авторизации с валидными данными"""

        response = self.api.login(
            auth_user_payload
        )

        response_data = response.json()
        print(response_data)

        assert response.status_code == 200, f"Ожидалcя - 200 ОК. Получен: {response.status_code}"
        assert "api_token" in response_data, "Нет токена в ответе"
        assert "unp" in response_data, "Нет УНП в ответе"

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ivalid_phone_number(self, auth_user_payload):
        """Валидации невалидного номера телефона"""

        payload = copy.deepcopy(auth_user_payload)
        payload["phone"] = "+375293397268"

        response = self.api.login(
            payload
        )

        response_data = response.json()
        print(response_data)

        assert response.status_code == 422, f"Ожидался - 422. Получен: {response.status_code}"
        assert "errors" in response_data, "Сообщение отсутсвует в теле ответа"
        assert "phone" in response_data["errors"], "Отсутсвует указание на поле с ошибкой в теле ответа"
        assert response_data["errors"]["phone"][0] == "Введенный номер телефона не связан ни с одним УНП"
    
    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_ivalid_password(self, auth_user_payload):
        """Валидации невалидного пароля"""
        
        payload = copy.deepcopy(auth_user_payload)
        payload["password"] = "123456789"

        response = self.api.login(
            payload
        )

        response_data = response.json()
        print(response_data.get("message"))

        assert response.status_code == 404, f"Ожидаемый статус - 404. Получен {response.status_code}"
        assert response_data.get("message")  == "Неверный номер телефона или пароль"

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_check_response_unp_with_db(self, connection_db, auth_user_payload):
        """Тест на сравнение УНП из ответа сервера и БД"""

        response = self.api.login(
            auth_user_payload
        )

        response_data = response.json()
        seller_unp = response_data.get("unp")

        seller_db_unp = connection_db.get_seller_unp_by_phone(auth_user_payload["phone"])

        assert seller_db_unp is not None, "UNP не найден в БД"
        assert seller_db_unp == seller_unp, "УНП не совпали"

    @pytest.mark.api_tests
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_check_reposnse_token_with_db(self, connection_db, auth_user_payload):
        """Тест на совпадения токена из ответа с токеном, записанным в БД"""
        
        response = self.api.login(
            auth_user_payload
        )

        resp_data = response.json()
        seller_unp = resp_data.get("unp")
        phone_num = auth_user_payload["phone"]

        api_token_db = connection_db.get_api_token_by_phone(seller_unp, phone_num)

        assert resp_data.get("api_token") == api_token_db, \
            f"Токены не совпадают. API:{resp_data["api_token"]}, БД:{api_token_db}"

    @pytest.mark.api_tests
    @pytest.mark.regression
    def test_empty_password_auth(self, auth_user_payload):
        """Валидация пустого поля для пароля"""

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

    