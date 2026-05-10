import pymysql
from config.config import DB

class DBClient:
    def __init__(self):
        self.db_conn = pymysql.connect(
        host=DB["host"],
        port=DB["port"],
        user=DB["user"],
        password=DB["password"],
        database=DB["database"],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
        )

    def get_one(self, sql, params=None):
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (params))

            return cursor.fetchone()
        
    def get_all(self, sql, params=None):
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, params)

            return cursor.fetchall()
        
    def sql_execute(self, sql, params=None):
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (params))

    def get_seller_id(self, api_token):
        sql_response = self.get_one(
            """SELECT sellers.id 
            FROM sellers 
            JOIN seller_accounts 
            ON sellers.unp = seller_accounts.unp 
            WHERE seller_accounts.api_token = %s""", 
            (api_token,)
        )

        return sql_response["id"] if sql_response else None
    
    def 