import pytest
import pymysql
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
def seller_id_from_db(connection_db, auth_user):
    with connection_db.cursor() as cursor:
        cursor.execute("SELECT unp FROM seller_accounts WHERE api_token = 'Zcp9Ywz84VRhgVuVC2kKFYnznXqMoYb0oEdtUkNMBPTXkVrYpQpJth9QsQ6jt8qOyYdixQ6f3UHN4CV2'")
        seller_unp = cursor.fetchone()

        cursor.execute("SELECT id FROM sellers WHERE unp = %s;", (seller_unp["unp"],))
        seller_id = cursor.fetchone()["id"]

    return seller_id

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

    response = api.login(auth_user_payload)

    return {
        "api_token": response.json()["api_token"],
        "unp": response.json()["unp"]
    }

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
def create_offer_draft_manually_payload_first():

    return {
            "step":1,
            "curStep":1,
            "name":"акция 3333",
            "options":1,
            "optionsArr":
                    [
                        {
                            "count_in_kit":2
                        }
                    ],
            "properties":{},
            "dimensions":{},
            "stepOptions":"1",
            "category_id":4830,
            "barcode":"48157647",
            "country_id":80,
            "importer_name":"",
            "is_adult":False,
            "prices":{},
            "installment_agreement":True,
            "vat":0,
            "images":[],
            "image_ids":[]
            }

@pytest.fixture
def create_offer_draft_manually_payload_third():
    return {
            "step":3,
            "curStep":3,
            "name":"Гель для теста",
            "options":1,
            "optionsArr":
                    [
                        {
                            "count_in_kit":2
                        }
                    ],
            "properties":
                    {
                        "149":5514
                    },
            "dimensions":
                    {
                        "length":"35",
                        "width":"55",
                        "height":"29",
                        "weight":"400"
                    },
            "stepOptions":"1",
            "brand_name":"Blocker",
            "category_id":4830,
            "barcode":"48146456",
            "brand_id":421,
            "manufacturer_name":"Годрик Гриффиндор",
            "country_id":80,
            "importer_name":"",
            "description":"Тестовый гель для душа",
            "is_adult":False,
            "prices":
                    {
                        "price":"2500"
                    },
            "installment_agreement":True,
            "vat":0,
            "images":[],
            "image_ids":[]
        }

@pytest.fixture
def create_offer_draft_bulk_payload():

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

