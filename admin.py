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
    return render_template('list_of_society_page.html', societies=data,area=['Urban','Rural'])

@admin_bp.route('/delete/<int:item_id>', methods=['POST'])
def reject_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Society_Detail WHERE sid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success','success':True, 'message': f'Item {item_id} rejected'})
    except Error as e:
        error_message = f"Error deleting item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500
    
@admin_bp.route('/edit/<int:row_id>', methods=['GET', 'POST'])
def edit_row(row_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Society_Detail WHERE sid = %s", (row_id,))
    row = cursor.fetchone()
    # print(row)
    cursor.close()

    if request.method == 'POST':
        society_name = request.form['s_name']
        Society_Address = request.form['s_address']
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
        
        values_tuple = (
                    society_name,
                    Society_Address,
                    Area,
                    City,
                    State,
                    Country,
                    Builder_Name,
                    Builder_Number,
                    Company_Name,
                    Total_Flats,
                    Total_Wings,
                    Total_Floor,
                    Empty_Flats,
                    Flat_on_each_Floor,
                    row_id
                )
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Society_Detail
            SET
                s_name = %s,
                s_address =%s,
                area =%s,
                city =%s,
                state = %s,
                country =%s,
                build_name =%s,
                build_no =%s,
                company_name =%s,
                total_flats =%s,
                total_wing =%s,
                total_floor =%s,
                empty_flat =%s,
                no_of_flat_on_each_floor =%s
            WHERE sid = %s;""", values_tuple)
        connection.commit()
        cursor.close()
        result = "Society Data Edited Successfully"


        return redirect('dashboard',result=result)

    return render_template('edit_row.html', row=row)

    
@admin_bp.route('/society_changes',methods=['POST','GET'])
def society_changes():
    # print("Hello")
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        society_name = request.form['s_name']
        Society_Address = request.form['s_address']
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
        
        # print("Received data:", society_name)
        user_name = session['name']
        photo_link = session.get('photo')

        if photo_link:
            image_data = fetch_image_from_google_drive(photo_link)

        # Encode image data to base64
        if image_data:
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            data = user_data(encoded_image,user_name,session['s_name'])

        connection = get_connection()
        if connection:

            if action == 'save':
                society_id = request.args.get('sid')
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
                        society_name, Society_Address, society_id, Area, City, State, Country, Total_Flats,
                        Empty_Flats, Total_Wings, Total_Floor, Flat_on_each_Floor, Builder_Name, Builder_Number,Company_Name, society_id)

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(save_query, values) 
                        connection.commit()
                        result = "Changes Saved"
                        # print(result)
                        connection.close()
                        return render_template('admin_dashboard.html',details = data, result=result)
                except Error as e:
                    print("Error:", e)
                    connection.close()
                    return render_template('admin_dashboard.html',details = data, result=e)
            elif action == 'add':
                insert_query = """
                INSERT INTO Society_Detail (s_name, s_address, area, city, state, country, total_flats, empty_flat, total_wing, total_floor, no_of_flat_on_each_floor, build_name, build_no, company_name) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                values = (
                        society_name, Society_Address, Area, City, State, Country, Total_Flats,
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
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 2 AND u.sid = s.sid and u.admin_approval=1")
        data = cursor.fetchall()

        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 2 AND u.sid = s.sid order by registration_date desc;")
        data2 = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_secretary_page.html', secretaries=data, approving_needed=data2)

@admin_bp.route('/delete_secretary/<item_id>', methods=['POST'])
def delete_security(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # List of tables to delete from
        tables = ['Maintenance_Display', 'Documents', 'Flat_details', 'Login', 'Users']
        
        for table in tables:
            try:
                cursor.execute(f'DELETE FROM {table} WHERE uid = %s;', (item_id,))
            except Error as e:
                print(f"Error deleting from {table}: {str(e)}")
                print(f"Data of user {item_id} has not been entered by treasurer in these tables")

        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'success': True, 'message': f'User {item_id} deleted'})
    
    except Error as e:
        error_message = f"Error deleting User {item_id}: {str(e)}"
        print(error_message)
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500

@admin_bp.route('/approve_secretary/<item_id>', methods=['POST'])
def approve_security(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # print("Hello")
        cursor.execute('UPDATE Users set admin_approval = 1, approval_date = NOW() where uid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Secretary {item_id} approved'})
    except Error as e:
        error_message = f"Error approving item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500
    
@admin_bp.route('/reject_secretary/<item_id>', methods=['POST'])
def reject_security(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # print("Hello")
        cursor.execute('UPDATE Users set admin_approval = 0, approval_date = NOW(), is_active = 0 where uid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Secretary {item_id} rejected'})
    except Error as e:
        error_message = f"Error rejecting item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500
    

@admin_bp.route('/security', methods=['GET'])
def security():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 5 AND u.sid = s.sid and u.admin_approval=1")
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
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s, Flat_Details as f WHERE u.role_id in (4,3,2) AND u.sid = s.sid and u.uid = f.uid and u.admin_approval=1")
        data = cursor.fetchall()
        # print(data)
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
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 3 AND u.sid = s.sid and admin_approval=1;")
        data = cursor.fetchall()
        # print(data)
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('list_of_treasurer_page.html', treasurers = data)



