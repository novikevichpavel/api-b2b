import pytest
import pymysql
import requests
from api.password_auth import UserAuth

@pytest.fixture
def connection_db():
    """Менеджер для создания подключения к БД"""
    
    with pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root123",
        database="marketplace-6-11",
        cursorclass=pymysql.cursors.DictCursor
    ) as db_connection:
        yield db_connection

@pytest.fixture
def auth_user_payload():
    """JSON для запроса на авторизацию"""

    return {
        "phone":"+375293397267",
        "password":"133322Qwe!@"
    }

@pytest.fixture
def auth_user(auth_user_payload):
    """Поолучение авторизационного токена"""

    api = UserAuth()
    # response = api.login(phone=auth_user_payload["phone"], password=auth_user_payload["password"])
    response = api.login(auth_user_payload)
    token = response.json()["api_token"]

    return token

@pytest.fixture
def create_offer_payload():
    """JSON для запроса на создание товара"""
    
    return {
            "offers": [
                        {
                                "name":"Тест товар Тест",
                                "optionsArr":[
                                            {
                                                "count_in_kit":2
                                            }
                                           ],
                                "properties":{
                                                "149":5514
                                            },
                                "stock":"50",
                                "dimensions":{
                                                "length":"12",
                                                "width":"12",
                                                "height":"12",
                                                "weight":"500"
                                            },
                                "brand_name":"Blocker",
                                "category_id":4830,
                                "barcode":"10000060",
                                "brand_id":42950,
                                "manufacturer_name":"EMALL",
                                "country_id":80,
                                "importer_name":"",
                                "description":"test_create_offer_api_test",
                                "is_adult":False,
                                "prices":{
                                            "price":"2500"
                                        },
                                "installment_agreement":True,
                                "vat":0,
                                "count_in_kit":"",
                                "service_centres":"",
                                "image_ids":[
                                                "1897120",
                                                "1897121",
                                                "1897122",
                                                "1897123"
                                            ]
                            }
                        ]           
                }      

@pytest.fixture
def create_offer_draft_payload():

    return {
            "offer_drafts":
                    [
                        {"name":"Гель для теста",
                         "category_id":4830,
                         "barcode":"10000061",
                         "brand_id":327,
                         "brand_name":"Добрый",
                         "country_id":80,
                         "inner_article":None,
                         "manufacturer_name":"Годрик грифендор",
                         "composition":None,
                         "storage_period":None,
                         "description":"Для теста",
                         "dimensions":
                                    {
                                        "length":55,
                                        "width":55,
                                        "height":55,
                                        "weight":500
                                    },
                        "count_in_kit":None,
                        "importer_name":None,
                        "service_centres":None,
                        "is_adult":True,
                        "warranty_unit":None,
                        "warranty_value":None,
                        "prices":
                                {
                                    "price":2500,
                                    "old_price":None
                                },
                        "properties":
                                {
                                    "149":5514,
                                    "1700":"1",
                                    "1755":"1000"
                                },
                        "vat":10,
                        "installment_agreement":True,
                        "images":
                                [
                            "https://pcdn.goldapple.ru/p/p/30323900018/web/696d674d61696e5064708ddc3ecc3059ce0.jpg",
                            "https://pcdn.goldapple.ru/p/p/30323900018/web/696d674d61696e5064708ddc3ecc3059ce0.jpg",
                            "https://pcdn.goldapple.ru/p/p/30323900018/web/696d674d61696e5064708ddc3ecc3059ce0.jpg",
                            "https://pcdn.goldapple.ru/p/p/30323900018/web/696d674d61696e5064708ddc3ecc3059ce0.jpg"
                                ],
                        "stock":5
                        }
                        ]
                }     