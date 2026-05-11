# import pytest
# from api.offers import OffersAPI
# import copy


# class TestProduct:

#     api = OffersAPI()

#     @pytest.mark.api_tests
#     @pytest.mark.smoke
#     @pytest.mark.regression
#     def test_create_offer(self, auth_user, create_offer_payload, connection_db):
#         """Тест создания товара с валидными данными"""

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=create_offer_payload
#         )

#         response_data = response.json()

#         offer_id = response_data["offer_ids"][0]

#         offer_db = connection_db.get_offer_by_id(offer_id,)
#         seller_id = connection_db.get_seller_id_by_token(auth_user["api_token"])

#         assert response.status_code == 201, f"Ожидася статус - 201, получен {response.status_code}"
#         assert "offer_ids" in response_data, "ID товара отсутсвует в ответе от сервера"
#         assert isinstance(response_data["offer_ids"][0], int), "ID товара должно быть числовым значением"
#         assert offer_db["id"] == offer_id, f"ID товара БД не совпадает с ID API. БД: {offer_db["id"]}"
#         assert seller_id == offer_db["seller_id"], f"ID на товар в offers: {offer_db["seller_id"]}, \
#             id в sellers: {seller_id}"
    
#     @pytest.mark.api_tests
#     @pytest.mark.regression
#     def test_repeat_create_same_offer(self, auth_user, create_offer_payload, connection_db):
#         """Тест на валидацию при создании дублируещего товара или товара, если бракод уже присвоен другому товару"""
        
#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=create_offer_payload
#         )

#         response_data = response.json()

#         barcode_count = connection_db.get_offer_count_by_barcode(create_offer_payload["offers"][0]["barcode"],)

#         assert response.status_code == 422, f"Ожидался: 422. Получен: {response.status_code}"
#         assert "errors" in response_data, "Нет валдиацинного сообщени]"
#         assert "offers.0.barcode" in response_data["errors"], "Нет указания на товар с ошибкой"
#         assert response_data["errors"]["offers.0.barcode"][0] == \
#             "Такой штрихкод уже существует для ваших товаров, проверьте правильность ввода"
#         assert barcode_count == 1, f"Несколько записей с таким баркодом. Кол-во строк: {barcode_count}. \
#             Баркод: {create_offer_payload["offers"][0]["barcode"]}"

#     @pytest.mark.api_tests
#     @pytest.mark.regression
#     @pytest.mark.parametrize("level", [1, 2])
#     def test_invalid_category_level(self, auth_user, create_offer_payload, connection_db, level):
#         """Тест на валидацию при создании товара с категоряими 1 и 2 уровня"""

#         category_level = connection_db.get_category_id_by_level(level)["id"]

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["category_id"] = category_level

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=payload
#         )

#         response_data = response.json()

#         offer_db = connection_db.get_offer_by_cat_id(category_level)

#         assert response.status_code == 422, f"Ожидаемый статус - 422. Получен: {response.status_code}"
#         assert "errors" in response_data, f"Валидационное сообщение отсутствует"
#         assert "offers.0.category_id" in response_data["errors"], "Отсутствует указание на товар в валидацинном сообщении"
#         assert offer_db is None, f"Ответ из БД: {offer_db}"

#     @pytest.mark.api_tests
#     @pytest.mark.smoke
#     @pytest.mark.regression
#     def test_requiered_properties(self, auth_user, create_offer_payload, connection_db):
#         """Тест на валидацию, если не заданы обязательные характеристики"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["properties"] = {}
#         payload["offers"][0]["barcode"] = "10000061"    

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=payload
#         )

#         response_data = response.json()

#         response_keys = list(response_data["errors"].keys())[0]

#         def extract_property(property_id):
#             return int(property_id.split(".")[-1])
        
#         property_id = extract_property(response_keys)

#         property_required_status = connection_db.get_property_required_status(create_offer_payload["offers"][0]["category_id"], property_id)

#         assert response.status_code == 422, f"Ожидался: 422. Получен: {response.status_code}"
#         assert "errors" in response_data, "Нет сообщения об ошибке"
#         assert "offers.0.properties.149" in response_data["errors"], "Нет указания на характеристику"
#         assert property_required_status["is_required"] == 1, f"Характеристика не обязательна. Параметр в БД: {property_required_status['is_required']}"

#     @pytest.mark.api_tests
#     @pytest.mark.smoke
#     @pytest.mark.regression
#     def test_check_importer_name_is_required(self, auth_user, create_offer_payload, connection_db):
#         """Тест на обязательность заполнения поля 'importer_name', если 'coutry_id' != 80"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["country_id"] = 1

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=payload
#         )

#         response_data = response.json()

#         assert response.status_code == 422, f"Ожидался: 422. Получен: {response.status_code}"
#         assert "errors" in response_data, "Нет текста ошибки в ответе"
#         assert "offers.0.importer_name" in response_data["errors"], "Нет указания на поле в ответе"
#         assert response_data["errors"]["offers.0.importer_name"][0] == \
#             'Поле "offers.0.importer_name" обязательно для заполнения, когда offers.0.country_id не равно 80.'
#         assert payload["offers"][0]["country_id"] != 80

#     @pytest.mark.api_tests
#     @pytest.mark.smoke
#     @pytest.mark.regression
#     def test_num_barcode(self, auth_user, create_offer_payload, connection_db):
#         """Тест на создание товара с невалидным баркодом. Передано числовое значение"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["barcode"] = 16634560

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=payload
#         )

#         barcode = str(payload["offers"][0]["barcode"])

#         response_data = response.json()

#         db_data = connection_db.get_offer_by_barcode(barcode)

#         assert response.status_code == 422, f"Ожидался: 422. Получен: {response.status_code}"
#         assert "errors" in response_data, "Нет валидации ошибки"
#         assert "offers.0.barcode" in response_data["errors"], "Нет указания на строку с ошибкой в ответе"
#         assert response_data["errors"]["offers.0.barcode"][0] == "Значение поля должно быть строкой"
#         assert db_data == None, f"В ответе из БД содержатся данные по товару: {db_data['id']}"

#     @pytest.mark.api_tests
#     @pytest.mark.smoke
#     @pytest.mark.regression
#     @pytest.mark.parametrize("barcode", ["1847563", "184756376"])
#     def test_invalid_barcode(self, auth_user, create_offer_payload, connection_db, barcode):
#         """Валидация неправильного баркода"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["barcode"] = barcode

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user["api_token"]},
#             payload=payload
#         )

#         response_data = response.json()

#         db_data = connection_db.get_offer_by_barcode(payload["offers"][0]["barcode"])

#         assert response.status_code == 422, f"Ожидался: 422. Получен: {response.status_code}"
#         assert "errors" in response_data, "Нет валидация ошибки"
#         assert "offers.0.barcode" in response_data["errors"], "Нет указания на строку с ошибкой в ответе"
#         assert response_data["errors"]["offers.0.barcode"][0] == \
#             "Разрешен ввод штрихкода форматов EAN-8 (8 цифр), EAN-13 (13 цифр), UPC (12 цифр)"
#         assert db_data is None, f"В БД содержатся данные по товару с id: {db_data['id']}"
