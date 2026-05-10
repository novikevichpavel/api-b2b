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
            cursor.execute(sql, params)

            return cursor.fetchone()
        
    def get_all(self, sql, params=None):
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, params)

            return cursor.fetchall()
        
    def sql_execute(self, sql, params=None):
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, params)

    def get_seller_id_by_token(self, api_token):
        sql_response = self.get_one(
            """SELECT sellers.id 
            FROM sellers 
            JOIN seller_accounts 
            ON sellers.unp = seller_accounts.unp 
            WHERE seller_accounts.api_token = %s""", 
            (api_token,)
        )

        return sql_response["id"] if sql_response else None
    
    def get_offer_by_barcode(self, barcode):
        return (
            self.get_one("SELECT * FROM offers WHERE barcode = %s", (barcode,))
        )
    
    def get_offer_by_id(self, offer_id):
        return (
            self.get_one("SELECT * FROM offers WHERE id = %s", (offer_id,))
        )
    
    def get_property_required_status(self, category_id, property_id):
        return (
            self.get_one("SELECT is_required FROM category_properties WHERE category_id = %s AND property_id = %s", (category_id, property_id,))
        )
    
    def get_category_id_by_level(self, category_level):
        return (
            self.get_one("SELECT id FROM categories WHERE level = %s", (category_level,))
        )
    
    def get_offer_by_cat_id(self, category_id):
        return(
            self.get_one("SELECT * FROM offers WHERE category_id = %s", (category_id,))
        )
    
    def get_offer_count_by_barcode(self, barcode):
        return(
            self.get_one("SELECT COUNT(*) AS count FROM offers WHERE barcode = %s", (barcode,))["count"]
        )
    
    def close(self):
        self.db_conn.close()