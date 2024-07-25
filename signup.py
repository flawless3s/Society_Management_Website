from flask import Blueprint, request, render_template, jsonify
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
        # print(role_id)
        try:
            signup_query_1 = "INSERT INTO Users (sid, role_id, uid, name, email, phone) VALUES(%s,%s,%s,%s,%s,%s);"
            cursor.execute(signup_query_1,(Society_id,role_id,user_id,name,email,phone))

            signup_query_2 = "INSERT INTO Login (role_id, uid, password) VALUES(%s,%s,%s);"
            cursor.execute(signup_query_2,(role_id,user_id,password))

            if role_id != '5':
                signup_query_3 = "INSERT INTO Flat_details (uid,sid,flat_no) VALUES(%s,%s,%s);"
                cursor.execute(signup_query_3,(user_id,Society_id,flat_no))

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
    
@signup_bp.route('/check_value', methods=['POST'])
def check_value():
    data = request.get_json()
    society = data['values']['society']
    flat_no = data['values']['flat_no']
    uid = data['values']['uid']
    connection = get_connection()
    cursor = connection.cursor()
    try:
        flat_no_query = "Select COUNT(1) from Flat_details where flat_no=%s and sid =%s;"
        cursor.execute(flat_no_query,(flat_no,society))
        flat_exists = cursor.fetchone()

        userid_no_query = "Select COUNT(1) from Users where uid =%s;"
        cursor.execute(userid_no_query,(uid,))
        uid_exists = cursor.fetchone()


    except Error as e:
        print(f"An error occurred while checking details: {e}", "danger")
     
    return jsonify({
        'flat_noExists': flat_exists,
        'uidExists': uid_exists
    })