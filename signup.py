from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from mysql.connector import Error
from database_connection import get_connection

signup_bp = Blueprint('signup', __name__, url_prefix='/signup')

@signup_bp.route('/', methods=['GET','POST'])
def signup():
    connection = get_connection()
    cursor = connection.cursor()
    if request.method == 'GET':
        try:
            cursor.execute("SELECT sid, CONCAT(s_name, ' - ', city, ', ', state) AS society_info FROM Society_Detail;")
            data = cursor.fetchall()

        except Error as e:
            print(f"An error occurred while fetching society details: {e}", "danger")
            data = []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return render_template('signup.html',societies = data)
    if request.method == 'POST':
        Society_id = request.form['society']
        role_id = request.form['role']
        user_id = request.form['uid']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone_no']
        password = request.form['password']
        flat_no = request.form['flat_no']
        sec_duty = request.form['sec_duty'] if request.form['sec_duty'] else 'None'
        print("Data:", sec_duty)
        try:
            signup_query_1 = "INSERT INTO Users (sid, role_id, uid, name, email, phone, security_duty) VALUES(%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(signup_query_1,(Society_id,role_id,user_id,name,email,phone,sec_duty))

            signup_query_2 = "INSERT INTO Login (role_id, uid, password) VALUES(%s,%s,%s);"
            cursor.execute(signup_query_2,(role_id,user_id,password))

            if sec_duty == 'None' and role_id != 5:
                signup_query_3 = "INSERT INTO Flat_details (uid,flat_no) VALUES(%s,%s);"
                cursor.execute(signup_query_3,(user_id,flat_no))

            connection.commit()
            print("Signup Successful")

        except Error as e:
            print(f"An error occurred while submitting details: {e}", "danger")
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return render_template('waiting_page.html')

