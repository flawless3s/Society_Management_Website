from flask import request, render_template, Blueprint, session,redirect, url_for, flash, jsonify
from mysql.connector import Error
from database_connection import get_connection

treasurer_bp = Blueprint('treasurer',__name__,url_prefix='/treasurer')

@treasurer_bp.route('/',methods=['GET'])
def list_members():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Flat_Details as f WHERE u.role_id in (4,2,3) AND u.uid = f.uid and u.sid=%s and u.admin_approval=1;",(session['sid'],))
        data = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching member details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_member_page_treasurer.html', members = data)


@treasurer_bp.route('/maintenance',methods=['GET'])
def maintenance_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("Select * from Users as u Join flat_details as f on u.uid = f.uid Join Maintenance_Display as m on u.uid = m.uid where u.sid=%s",(session['sid'],))
        data = cursor.fetchall()
        # print(data)
    except Error as e:
        print(f"An error occurred while fetching maintenance details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('maintenance_treasurer_page.html', members = data)

@treasurer_bp.route('/edit/<int:row_id>', methods=['GET', 'POST'])
def edit_row(row_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Maintenance_Display as m, Flat_details as f WHERE m.mid = %s and m.uid = f.uid", (row_id,))
    row = cursor.fetchone()
    # print(row)
    cursor.close()

    if request.method == 'POST':
        flat_no = request.form['flat_no']
        amt = request.form['maintenance_amt']
        month = request.form['month']
        year = request.form['year']
        
        

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("Select u.uid from Users as u Join Flat_details as f on u.uid = f.uid Join Society_detail as s on u.sid = s.sid where s.sid=%s and f.flat_no = %s;",(session['sid'],flat_no))
        new_user_id = cursor.fetchone()

        values_tuple = (new_user_id[0], amt, month, year, row_id)
        # print(values_tuple)
        cursor.execute("""
            UPDATE Maintenance_Display
            SET
                uid = %s,
                bill_amt = %s,
                bill_month = %s,
                bill_year = %s
            WHERE mid = %s;""", values_tuple)
        connection.commit()
        cursor.close()
        result = "Maintenance Data Edited Successfully"


        return redirect(url_for('dashboard',result=result))

    return render_template('treasurer_edit_row.html', row=row)

@treasurer_bp.route('/issuemaintenance',methods=['GET','POST'])
def maintenance_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        flat_no = request.form['flat_no']
        amt = request.form['maintenance_amt']
        month = request.form['month']
        year = request.form['year']
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("Select u.uid from Users as u Join Flat_details as f on u.uid = f.uid Join Society_detail as s on u.sid = s.sid where s.sid=%s and f.flat_no = %s;",(session['sid'],flat_no))
            user_id = cursor.fetchone()
            cursor.execute("INSERT INTO Maintenance_Display (sid, uid, bill_amt, bill_month, bill_year)VALUES (%s,%s,%s,%s,%s);",(session['sid'],user_id[0],amt,month,year))
            connection.commit()
            result = "Bill Issued Successfully"
            return redirect(url_for('dashboard',result=result))
        except Error as e:
            print(f"An error occurred while inserting maintenance details: {e}", "danger")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('maintenance_form_treasurer.html')

@treasurer_bp.route('/check_value', methods=['POST'])
def check_value():
    # print("Hello")
    data = request.get_json()
    flat_no = data['values']['flat_no']
    connection = get_connection()
    cursor = connection.cursor()
    try:
        flat_no_query = "Select COUNT(1) from Flat_details where flat_no=%s and sid =%s;"
        cursor.execute(flat_no_query,(flat_no,session['sid']))
        flat_exists = cursor.fetchone()


    except Error as e:
        print(f"An error occurred while checking details: {e}", "danger")
     
    return jsonify({
        'flat_noExists': flat_exists,
    })


#Treasurer Rent
@treasurer_bp.route('/rent',methods=['GET'])
def rent():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("Select * from Users as u Join flat_details as f on u.uid = f.uid Join Maintenance_Display as m on u.uid = m.uid where u.sid=%s",(session['sid'],))
        data = cursor.fetchall()
        # print(data)
    except Error as e:
        print(f"An error occurred while fetching maintenance details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('maintenance_treasurer_page.html', members = data)






    