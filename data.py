from mysql.connector import Error
from database_connection import get_connection
from flask import session
from datetime_checker import check_time
class user_data:
    def __init__(self, image, username, society_name):
        self.image = image
        self.username = username
        self.society_name = society_name



def convert_tuples_to_objects(tuple_list, cls):
    return [cls(*t) for t in tuple_list]



    


class Item:
    def __init__(self, item_id, sid, flat_no, package_desc, time_arrival, date_arrival, permission=False):
        self.item_id = item_id
        self.sid = sid
        self.flat_no = flat_no
        self.package_desc = package_desc
        self.time_arrival = time_arrival
        self.date_arrival = date_arrival
        self.permission = permission

    def __repr__(self):
        return (f"Item(package_arrival_id={self.item_id}, sid={self.sid}, flat_no='{self.flat_no}', "
                f"package_desc='{self.package_desc}', time_arrival='{self.time_arrival}', "
                f"date_arrival='{self.date_arrival}', permission={self.permission})")


def fetch_package_data():
    connection = get_connection()
    if connection:
        try:
            flatno_query = "Select flat_no from Flat_details where uid=%s;"
            value = (session['user_id'],)


            with connection.cursor() as cursor:
                cursor.execute(flatno_query,value)
                result = cursor.fetchone()
                print(result)

                if result:
                    package_query = "Select * from MyGate_Permission_Security where sid=%s and flat_no=%s and permission = '0';"
                    value = (session['sid'],session['flat_no'])
            

                    cursor.execute(package_query, value)
                    # print("Hello")
                    result = cursor.fetchall()
                    print(result)
                    return convert_tuples_to_objects(result,Item)
                else:
                    return [('Could not fetch data')] 

        except Error as e:
            return [('Could not fetch data')]        
    else:
        return 'Database connection failed'
    


class Document:
    def __init__(self, uid, document_id, doc_name, document_file):
        self.uid = uid
        self.document_id = document_id
        self.doc_name = doc_name
        self.document_file = document_file
    
    def __repr__(self):
        return (f"Document(uid='{self.uid}', document_id={self.document_id}, "
                f"doc_name='{self.doc_name}', document_file=<{len(self.document_file)} bytes>)")



def fetch_document_data():
    connection = get_connection()
    if connection:
        try:
            flatno_query = "Select * from Documents where uid=%s;"
            value = (session['user_id'],)


            with connection.cursor() as cursor:
                cursor.execute(flatno_query,value)
                result = cursor.fetchall()

                return convert_tuples_to_objects(result,Document)

        except Error as e:
            return [('Could not fetch data')]        
    else:
        return 'Database connection failed'

   



class MyGatePermissionSecurity:
    def __init__(self, item_id, sid, flat_no, package_desc, time_arrival, date_arrival, permission=False):
        self.item_id = item_id
        self.sid = sid
        self.flat_no = flat_no
        self.package_desc = package_desc
        self.time_arrival = time_arrival
        self.date_arrival = date_arrival
        self.permission = permission

    def __str__(self):
        return (f"MyGatePermissionSecurity(item_id={self.item_id}, sid={self.sid}, "
                f"flat_no='{self.flat_no}', package_desc='{self.package_desc}', "
                f"time_arrival='{self.time_arrival}', date_arrival='{self.date_arrival}', "
                f"permission={self.permission})")
    

def fetch_package_permission():
    check_time()
    connection = get_connection()
    if connection:
        try:
            permission_query = "Select * from MyGate_Permission_Security where sid=%s;"
            value = (session['sid'],)
            # print(session['sid'])
            
            with connection.cursor() as cursor:
                cursor.execute(permission_query, value)
                result = cursor.fetchall()
                return convert_tuples_to_objects(result,MyGatePermissionSecurity)


        except Error as e:
            return [('Could not fetch data')]        
    else:
        return 'Database connection failed'

class MyGateResident:
    def __init__(self, package_id, sid, flat_no, package_desc, time_arrival, date_arrival, permission=False):
        self.package_id = package_id
        self.sid = sid
        self.flat_no = flat_no
        self.package_desc = package_desc
        self.time_arrival = time_arrival
        self.date_arrival = date_arrival
        self.permission = permission

    def __str__(self):
        return (f"MyGatePermissionSecurity(item_id={self.item_id}, sid={self.sid}, "
                f"flat_no='{self.flat_no}', package_desc='{self.package_desc}', "
                f"time_arrival='{self.time_arrival}', date_arrival='{self.date_arrival}', "
                f"permission={self.permission})")
    

   
def fetch_package_advance():
    connection = get_connection()
    if connection:
        try:
            permission_query = "Select * from MyGate_Resident where sid=%s and resident_permission=1;"
            value = (session['sid'],)
            
            with connection.cursor() as cursor:
                cursor.execute(permission_query, value)
                result = cursor.fetchall()
                print(result)
                return convert_tuples_to_objects(result,MyGateResident)

        except Error as e:
            return [(e,)]        
    else:
        return 'Database connection failed'

