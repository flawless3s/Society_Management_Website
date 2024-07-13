from flask import Flask, request, render_template, Blueprint, session,redirect, url_for, flash
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
        cursor.execute("SELECT * FROM Users as u, Flat_Details as f WHERE u.role_id = 4 AND u.uid = f.uid and u.sid=%s;",(session['sid'],))
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
        print(data)
    except Error as e:
        print(f"An error occurred while fetching maintenance details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('maintenance_treasurer_page.html', members = data)

@treasurer_bp.route('/issuemaintenance',methods=['GET','POST'])
def maintenance_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        flat_no = request.form['flat_no']
        amt = request.form['maintenance_amt']
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("Select u.uid from Users as u Join Flat_details as f on u.uid = f.uid Join Society_detail as s on u.sid = s.sid where s.sid=%s and f.flat_no = %s;",(session['sid'],flat_no))
            user_id = cursor.fetchone()
            cursor.execute("INSERT INTO Maintenance_Display (sid, uid, bill_amt)VALUES (%s,%s,%s);",(session['sid'],user_id[0],amt))
            connection.commit()
            return redirect(url_for('dashboard'))
        except Error as e:
            print(f"An error occurred while inserting maintenance details: {e}", "danger")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    return render_template('maintenance_form_treasurer.html')

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
        print(data)
    except Error as e:
        print(f"An error occurred while fetching maintenance details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('maintenance_treasurer_page.html', members = data)






    