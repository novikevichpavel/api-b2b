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
            self.get_one(
                "SELECT * FROM offers WHERE barcode = %s", 
                (barcode,)
                )
        )
    
    def get_offer_by_id(self, offer_id):
        return (
            self.get_one(
                "SELECT * FROM offers WHERE id = %s", 
                (offer_id,)
                )
        )
    
    def get_property_required_status(self, category_id, property_id):
        return (
            self.get_one(
                "SELECT is_required FROM category_properties WHERE category_id = %s AND property_id = %s", 
                (category_id, property_id,)
                )
        )
    
    def get_category_id_by_level(self, category_level):
        return (
            self.get_one(
                "SELECT id FROM categories WHERE level = %s", 
                (category_level,)
                )
        )
    
    def get_offer_by_cat_id(self, category_id):
        return(
            self.get_one(
                "SELECT * FROM offers WHERE category_id = %s", 
                (category_id,)
                )
        )
    
    def get_offer_count_by_barcode(self, barcode):
        return(
            self.get_one(
                "SELECT COUNT(*) AS count FROM offers WHERE barcode = %s", 
                (barcode,))["count"]
        )
    
    def get_seller_unp_by_phone(self, phone_num):
        return(
            self.get_one(
                "SELECT unp FROM seller_accounts WHERE phone = %s", 
                (phone_num,))["unp"]
        )

    def get_api_token_by_phone(self, seller_unp, phone_num):
        return (
            self.get_one(
                "SELECT api_token FROM seller_accounts WHERE unp = %s AND phone = %s", 
                (seller_unp, phone_num,))["api_token"]
        )
    
    def update_offer_status(self, status_id, offer_id):
        return (
            self.sql_execute(
                "UPDATE offers SET status_id = %s WHERE id = %s",
                (status_id, offer_id)
            )
        )
    
    def get_property_option_id(self, offer_id, property_id):
        return (
            self.get_one(
            """
            SELECT opv.property_option_id
            FROM offer_properties op
            JOIN offer_property_values opv
            ON opv.offer_property_id = op.id
            WHERE op.offer_id = %s
            AND op.property_id = %s
            """,
            (offer_id, property_id))
        )

    def close(self):
        self.db_conn.close()