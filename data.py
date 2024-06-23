from mysql.connector import Error
from database_connection import get_connection
from flask import session
class user_data:
    def __init__(self, image, username):
        self.image = image
        self.username = username


class Maintenance:
    def __init__(self,mid, sid, uid, item_name, bill_amt, bill_month, bill_year, payment_status, payment_date=None):
        self.mid = mid
        self.sid = sid
        self.uid = uid
        self.item_name = item_name
        self.bill_amt = bill_amt
        self.bill_month = bill_month
        self.bill_year = bill_year
        self.payment_status = payment_status
        self.payment_date = payment_date

    def __repr__(self):
        return f"MaintenanceDisplay(sid={self.sid}, uid={self.uid}, item_name='{self.item_name}', bill_amt={self.bill_amt}, bill_month='{self.bill_month}', bill_year={self.bill_year}, payment_status={self.payment_status}, payment_date={self.payment_date})"



def convert_tuples_to_objects(tuple_list, cls):
    return [cls(*t) for t in tuple_list]



def fetch_maintenance_data():

    connection = get_connection()
    if connection:
        try:
            Maintenance_query = "Select * from maintenance_display where uid=%s ;"
            value = (session['user_id'],)
            # print(session['user_id'])

            with connection.cursor() as cursor:
                cursor.execute(Maintenance_query,value)
                result = cursor.fetchall()
                # print(result)
                return convert_tuples_to_objects(result,Maintenance)
        except Error as e:
            return [('Could not fetch data')]        
    else:
        return 'Database connection failed'