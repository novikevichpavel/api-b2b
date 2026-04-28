# import pytest
# import requests
# import pymysql
# import time
# from api.offers import OffersAPI
# import copy


# class TestProduct:

#     api = OffersAPI()

#     def test_create_offer(self, auth_user, create_offer_payload, connection_db, ):
#         """Тест создания товара с валидными данными"""

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user},
#             payload=create_offer_payload
#         )

#         response_data = response.json()
#         print(f"ID созданного товара: {response_data["offer_ids"][0]}")

#         offer_id = response_data["offer_ids"][0]

#         with connection_db.cursor() as cursor:
#             # Заменить хардкод на переменную offer_id
#             cursor.execute("SELECT * FROM offers WHERE id = 9583754")
#             db_data = cursor.fetchone()

#             cursor.execute(
#                 "SELECT unp FROM seller_accounts WHERE api_token = 'Zcp9Ywz84VRhgVuVC2kKFYnznXqMoYb0oEdtUkNMBPTXkVrYpQpJth9QsQ6jt8qOyYdixQ6f3UHN4CV2'"
#                 ) #(auth_user)
#             seller_unp = cursor.fetchone()["unp"]

#             cursor.execute("SELECT id FROM sellers WHERE unp = %s", (seller_unp,))
#             sellers_id = cursor.fetchone()["id"]

#         print(f"ID созданного товара в БД: {db_data["id"]}")

#         assert response.status_code == 201, f"Ожидася статус - 201, получен {response.status_code}"
#         assert "offer_ids" in response_data, "ID товара отсутсвует в ответе от сервера"
#         assert len(response_data["offer_ids"]) > 0, "Список созданных товаров пуст"
#         assert isinstance(response_data["offer_ids"][0], int), "ID товара должно быть числовым значением"
#         # Тут тоже на переменную поменять
#         assert db_data["id"] == 9583754, f"ID товара в БД не совпадает с ID в ответе от серевера. ID из БД {db_data["id"]}"
#         assert db_data is not None, f"В БД нет товара с id: 9583754"
#         assert sellers_id == db_data["seller_id"], f"ID не совпадают. ID для товара в таблие offers: {db_data["seller_id"]}, id полученный из таблицы sellers: {sellers_id}"

#         time.sleep(2)

#     def test_repeat_create_same_offer(self, auth_user, create_offer_payload, connection_db):
#         """Тест на валидацию при содании дублируещего товара или товара, если бракод уже присвоен другому товару"""
        
#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user},
#             payload=create_offer_payload
#         )

#         response_data = response.json()

#         print(response_data["errors"]["offers.0.barcode"][0])

#         with connection_db.cursor() as cursor:
#             cursor.execute("SELECT COUNT(*) AS barcode_list FROM offers WHERE barcode = %s", (create_offer_payload["offers"][0]["barcode"]))
#             barcode_list = cursor.fetchone()["barcode_list"]

#         assert response.status_code == 422, f"Ожидался статус - 422, получен {response.status_code}"
#         assert "errors" in response_data, "Отсутствует валдиацинное сообщение"
#         assert "offers.0.barcode" in response_data["errors"], "Отсутсвует указание на товар с ошибкой"
#         assert response_data["errors"]["offers.0.barcode"][0] == \
#             "Такой штрихкод уже существует для ваших товаров, проверьте правильность ввода"
#         assert barcode_list == 1, f"Несколько записей с таким баркодом. Кол-во строк: {barcode_list}. \
#             Баркод: {create_offer_payload["offers"][0]["barcode"]}"

#     def test_create_offer_top_category_level_one(self, auth_user, create_offer_payload, connection_db):
#         """Тест на валидацию при создании товара с уровнем категории: 1"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["category_id"] = 3933

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user},
#             payload=payload
#         )

#         response_data = response.json()
#         print(response_data["errors"]["offers.0.category_id"][0])

#         with connection_db.cursor() as cursor:
#             cursor.execute(
#                 "SELECT unp FROM seller_accounts WHERE api_token ='Zcp9Ywz84VRhgVuVC2kKFYnznXqMoYb0oEdtUkNMBPTXkVrYpQpJth9QsQ6jt8qOyYdixQ6f3UHN4CV2'"
#                 )
#             seller_unp = cursor.fetchone()["unp"]

#             cursor.execute("SELECT id FROM sellers WHERE unp = %s", (seller_unp,))
#             seller_id = cursor.fetchone()["id"]

#             cursor.execute("SELECT * FROM offers WHERE category_id = %s and seller_id = %s", 
#                            (payload["offers"][0]["category_id"], seller_id,))
#             db_response = cursor.fetchone()

#         assert db_response is None, f"Ответ из БД: {db_response}"
#         assert response.status_code == 422, f"Ожидаемый статус - 422. Получен: {response.status_code}"
#         assert "errors" in response_data, f"Валидационное сообщение отсутствует"
#         assert "offers.0.category_id" in response_data["errors"], "Отсутствует указание на товар в валидацинном сообщении"

#     def test_create_offer_top_category_level_two(self, auth_user, create_offer_payload, connection_db):
#         """Тест на валидацию при создании товара с уровнем категории: 2"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["category_id"] = 3898

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user},
#             payload=payload
#         )

#         response_data = response.json()
#         print(response_data["errors"]["offers.0.category_id"][0])

#         with connection_db.cursor() as cursor:
#             cursor.execute(
#                 "SELECT unp FROM seller_accounts WHERE api_token='Zcp9Ywz84VRhgVuVC2kKFYnznXqMoYb0oEdtUkNMBPTXkVrYpQpJth9QsQ6jt8qOyYdixQ6f3UHN4CV2'"
#                 )
#             seller_unp = cursor.fetchone()["unp"]

#             cursor.execute("SELECT id FROM sellers WHERE unp = %s", (seller_unp,))
#             seller_id = cursor.fetchone()["id"]

#             cursor.execute("SELECT * FROM offers WHERE category_id = %s and seller_id = %s", (payload["offers"][0]["category_id"], seller_id,))
#             db_response = cursor.fetchone()


#         assert response.status_code == 422, f"Ожидаемый статус - 422. Получен: {response.status_code}"
#         assert "errors" in response_data, f"Валидационное сообщение отсутствует"
#         assert "offers.0.category_id" in response_data["errors"], "Отсутствует указание на товар в валидацинном сообщении"
#         assert db_response is None, f"Ответ из БД: {db_response}"

#     def test_requiered_properties(self, auth_user, create_offer_payload, connection_db):
#         """Тест на валидацию, если не заданы обязательные характеристики"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["properties"] = {}
#         payload["offers"][0]["barcode"] = "10000061"    

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user},
#             payload=payload
#         )

#         response_data = response.json()
        
#         print(response_data)

#         response_keys = list(response_data["errors"].keys())[0]

#         def extract_property(property_id):
#             return int(property_id.split(".")[-1])
        
#         property_id = extract_property(response_keys)

#         print(property_id)

#         with connection_db.cursor() as cursor:
#             cursor.execute(
#                 "SELECT is_required FROM category_properties WHERE category_id = %s AND property_id = %s", 
#                 (create_offer_payload["offers"][0]["category_id"], property_id)
#                 )
#             db_data = cursor.fetchone()

#         print(db_data["is_required"])

#         assert response.status_code == 422, f"Ожидаемый статус - 422. Получен: {response.status_code}"
#         assert "errors" in response_data, "Отсутствует сообщение об ошибке"
#         assert "offers.0.properties.149" in response_data["errors"], "В ответ отсутствует указание на характеристику"
#         assert db_data["is_required"] == 1, f"Характеристика не является обязательной. Значение параметра в БД: {db_data["is_required"]}"

#     def test_check_importer_name_is_required(self, auth_user, create_offer_payload, connection_db):
#         """Тест на обязательность заполнения поля 'importer_name', если 'coutry_id' != 80"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["country_id"] = 1

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user},
#             payload=payload
#         )

#         response_data = response.json()
#         print(response_data["errors"]["offers.0.importer_name"][0])

#     def test_num_barcode(self, auth_user, create_offer_payload, connection_db):
#         """Тест на создание товара с невалидным баркодом. Передано числовое значение"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["barcode"] = 16634560

#         response = self.api.create_offer(
#             headers={"Apitoken": auth_user},
#             payload=payload
#         )

#         response_data = response.json()

#         print(response_data["errors"]["offers.0.barcode"][0])

#         with connection_db.cursor() as cursor:
#             cursor.execute(
#                 "SELECT * FROM offers WHERE barcode = %s",
#                 (payload["offers"][0]["barcode"])
#             )
#             db_data = cursor.fetchone()

#         print(db_data)

#         assert response.status_code == 422, f"Ожидаемый статус - 422. Получен {response.status_code}"
#         assert "errors" in response_data, "В ответе отсутсвует валидация ошибки"
#         assert "offers.0.barcode" in response_data["errors"], "Отсутствует указание на строку с ошибкой, в ответе от сервера"
#         assert response_data["errors"]["offers.0.barcode"][0] == "Значение поля должно быть строкой"
#         assert db_data == None, f"В ответе из БД содержатся данные по товару с id: {db_data["id"]}"

#     def test_invalid_barcode(self, auth_user, create_offer_payload, connection_db):
#         """Тест на создание товара с невалидным баркодом. Строковое значение"""

#         payload = copy.deepcopy(create_offer_payload)
#         payload["offers"][0]["barcode"] = "1847563"

#         response = self.api.create_offer(
#             headers={"Apitoken":auth_user},
#             payload=payload
#         )

#         response_data = response.json()

#         print(response_data["errors"]["offers.0.barcode"][0])

#         with connection_db.cursor() as cursor:
#             cursor.execute(
#                 "SELECT * FROM offers WHERE barcode = %s",
#                 (payload["offers"][0]["barcode"])
#             )
#             db_data = cursor.fetchone()

#         print

#         assert response.status_code == 422, f"Ожидаемый статус - 422. Получен {response.status_code}"
#         assert "errors" in response_data, "В ответе отсутсвует валидация ошибки"
#         assert "offers.0.barcode" in response_data["errors"], "Отсутствует указание на строку с ошибкой, в ответе от сервера"
#         assert response_data["errors"]["offers.0.barcode"][0] == "Разрешен ввод штрихкода форматов EAN-8 (8 цифр), EAN-13 (13 цифр), UPC (12 цифр)"
#         assert db_data == None, f"В ответе из БД содержатся данные по товару с id: {db_data["id"]}"

        



#     # def test_validation_vat_block():
#     #     """Тест на валидацю заполнения гарантийного блока, если параметр вкл"""

#     #     pass

    


