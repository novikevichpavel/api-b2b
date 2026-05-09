from config.env import (
    ENV,
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)

DB = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME
}

API_URLS = {
    "test": "https://api-test6-11.emall.by/api/b2b/v1"
}

API_BASE_URL = API_URLS.get(ENV, API_URLS["test"])