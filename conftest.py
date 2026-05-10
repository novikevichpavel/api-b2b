import pytest
from api.password_auth import UserAuth
from api.offers import OffersAPI
from config.config import DB
from db_client.db_client import DBClient


@pytest.fixture
def connection_db():
    """Менеджер для создания подключения к БД"""
    db_client = DBClient()
    yield db_client
    db_client.close()


@pytest.fixture
def create_offer_fixt(auth_user, create_offer_payload):
    """Фикстура создания товара"""
    api = OffersAPI()
    
    response = api.create_offer(
        headers={"Apitoken": auth_user["api_token"]},
        payload=create_offer_payload
    )

    assert response.status_code == 201

    return response.json()["offer_ids"][0]


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

    assert response.status_code == 200, "Не удалось авторизоваться"

    return {
        "api_token": response.json()["api_token"],
        "unp": response.json()["unp"]
    }


@pytest.fixture
def sms_auth(auth_user_payload):

    api = UserAuth()

    response = api.sms_login(auth_user_payload["phone"])


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
def create_offer_draft_manually_payload():
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

