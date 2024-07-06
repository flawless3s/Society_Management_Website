from flask import Blueprint, request, render_template, session, redirect, url_for, flash, jsonify
from mysql.connector import Error
import pymysql
from pymysql import Error
from database_connection import get_connection
from fetching_image import fetch_image_from_google_drive
from data import user_data
import base64

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/roles', methods=['GET'])
def roles():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('list_of_roles_page.html')

@admin_bp.route('/societies', methods=['GET'])
def society():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Society_Detail")
        data = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching society details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_society_page.html', societies=data)

@admin_bp.route('/delete/<int:item_id>', methods=['POST'])
def reject_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Hello")
        cursor.execute('DELETE FROM Society_Detail WHERE sid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Item {item_id} rejected'})
    except Error as e:
        error_message = f"Error deleting item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500
    
@admin_bp.route('society_changes',methods=['POST'])
def society_changes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        society_name = request.form['s_name']
        Society_Address = request.form['s_address']
        Society_id = request.form['sid']
        Area = request.form['area']
        City = request.form['city']
        State = request.form['state']
        Country = request.form['country']
        Total_Flats = request.form['total_flats']
        Empty_Flats = request.form['empty_flats']
        Total_Wings = request.form['total_wings']
        Total_Floor = request.form['total_floor']
        Company_Name = request.form['c_name']
        Flat_on_each_Floor = request.form['flat_on_each_floor']
        Builder_Name = request.form['build_name']
        Builder_Number = request.form['build_number']
        action = request.form['action']
        
        print("Received data:", society_name)
        user_name = session['name']
        photo_link = session.get('photo')

        if photo_link:
            image_data = fetch_image_from_google_drive(photo_link)

        # Encode image data to base64
        if image_data:
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            data = user_data(encoded_image,user_name)

        connection = get_connection()
        if connection:

            if action == 'save':
                save_query = """
                UPDATE Society_detail 
                SET 
                    s_name = %s,
                    s_address = %s,
                    sid = %s,
                    area = %s,
                    city = %s,
                    state = %s,
                    country = %s,
                    total_flats = %s,
                    empty_flat = %s,
                    total_wing = %s,
                    total_floor = %s,
                    no_of_flat_on_each_floor = %s,
                    build_name = %s,
                    build_no = %s,
                    company_name = %s
                WHERE 
                    sid = %s;
                """
                values = (
                        society_name, Society_Address, Society_id, Area, City, State, Country, Total_Flats,
                        Empty_Flats, Total_Wings, Total_Floor, Flat_on_each_Floor, Builder_Name, Builder_Number,Company_Name, Society_id)

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(save_query, values) 
                        connection.commit()
                        result = "Changes Saved"
                        print(result)
                        connection.close()
                        return render_template('admin_dashboard.html',details = data, result=result)
                except Error as e:
                    print("Error:", e)
                    connection.close()
                    return render_template('admin_dashboard.html',details = data, result=e)
            elif action == 'add':
                insert_query = """
                INSERT INTO Society_Detail (s_name, s_address, sid, area, city, state, country, total_flats, empty_flat, total_wing, total_floor, no_of_flat_on_each_floor, build_name, build_no, company_name) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                values = (
                        society_name, Society_Address, Society_id, Area, City, State, Country, Total_Flats,
                        Empty_Flats, Total_Wings, Total_Floor, Flat_on_each_Floor, Builder_Name, Builder_Number,Company_Name)

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(insert_query, values) 
                        connection.commit()
                        result="New Society Added"
                        connection.close()
                        return render_template('admin_dashboard.html',details = data, result=result)

                except Error as e:
                    print("Error:", e)
                    connection.close()
                    return render_template('admin_dashboard.html',details = data, result=e)

        else:
            return render_template('error.html', error="Database connection failed")

@admin_bp.route('/secretaries', methods=['GET'])
def secretary():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 2 AND u.sid = s.sid")
        data = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_secretary_page.html', secretaries=data)


@admin_bp.route('/security', methods=['GET'])
def security():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 5 AND u.sid = s.sid")
        data = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_security_page.html', securities = data)

@admin_bp.route('/member', methods=['GET'])
def member():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s, Flat_Details as f WHERE u.role_id = 4 AND u.sid = s.sid and u.uid = f.uid;")
        data = cursor.fetchall()
        print(data)
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_member_page.html', members = data)

@admin_bp.route('/treasurer', methods=['GET'])
def treasurer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 3 AND u.sid = s.sid;")
        data = cursor.fetchall()
        print(data)
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_treasurer_page.html', treasurers = data)



