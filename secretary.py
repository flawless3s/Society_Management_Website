from flask import Blueprint, request, render_template, session, redirect, url_for, flash, jsonify
from mysql.connector import Error 
from database_connection import get_connection

secretary_bp = Blueprint('secretary', __name__,url_prefix='/secretary')


@secretary_bp.route('/secretary_member', methods=['GET'])
def member():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s, Flat_Details as f WHERE u.role_id in (3,4) AND u.sid = s.sid and u.uid = f.uid and u.admin_approval = 1;")
        data = cursor.fetchall()
        
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s, Flat_Details as f WHERE u.role_id in (3,4) AND u.sid = s.sid and u.uid = f.uid order by registration_date desc;")
        data2 = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('approve_member_page.html', members = data, approving_needed = data2)

@secretary_bp.route('/delete/<item_id>', methods=['POST'])
def delete_item(item_id):
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
        error_message = f"Error deleting item {item_id}: {str(e)}"
        print(error_message)
        return jsonify({'status': 'error', 'message': error_message}), 500

    

@secretary_bp.route('/approve/<item_id>', methods=['POST'])
def approve_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Hello")
        cursor.execute('UPDATE Users set admin_approval = 1, approval_date = NOW() where uid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Item {item_id} approved'})
    except Error as e:
        error_message = f"Error approving item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500

@secretary_bp.route('/reject/<item_id>', methods=['POST'])
def reject_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Hello")
        cursor.execute('UPDATE Users set admin_approval = 0 and approval_date = NULL where uid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Item {item_id} rejected'})
    except Error as e:
        error_message = f"Error rejecting item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500
    

@secretary_bp.route('/security', methods=['GET'])
def security():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 5 AND u.sid = s.sid and admin_approval = 1")
        data = cursor.fetchall()

        cursor.execute("SELECT * FROM Users as u, Society_Detail as s WHERE u.role_id = 5 AND u.sid = s.sid order by registration_date desc;")
        data2 = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('approve_security_page.html', securities = data, approving_needed = data2)

@secretary_bp.route('/delete_security/<item_id>', methods=['POST'])
def delete_security(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Hello")
        cursor.execute('DELETE FROM Login WHERE uid = %s;', (item_id,))
        cursor.execute('DELETE FROM Users WHERE uid = %s;', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success','success': True, 'message': f'User {item_id} deleted'})
    except Error as e:
        error_message = f"Error deleting User {item_id}: {str(e)}"
        print(error_message)
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500

@secretary_bp.route('/approve_security/<item_id>', methods=['POST'])
def approve_security(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Hello")
        cursor.execute('UPDATE Users set admin_approval = 1, approval_date = NOW() where uid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Security {item_id} approved'})
    except Error as e:
        error_message = f"Error approving item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500
    
@secretary_bp.route('/reject_security/<item_id>', methods=['POST'])
def reject_security(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print("Hello")
        cursor.execute('UPDATE Users set admin_approval = 0 and approval_date = NULL where uid = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Security {item_id} rejected'})
    except Error as e:
        error_message = f"Error rejecting item {item_id}: {str(e)}"
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500
    

@secretary_bp.route('/notice', methods=['GET'])
def notice_editor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Notice WHERE sid=%s order by post_date desc;",(session['sid'],))
        data = cursor.fetchall()
    except Error as e:
        flash(f"An error occurred while fetching secretary details: {e}", "danger")
        data = []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('notice_edit_secretary.html', notices = data)

@secretary_bp.route('/update_notice', methods=['POST'])
def update_notice():
    data = request.json
    n_id = data['n_id']
    column = data['column']
    value = data['value']
    print(value)
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = f"UPDATE Notice SET {column} = %s WHERE n_id = %s"
        cursor.execute(sql, (value, n_id))
        connection.commit()
    connection.close()

    return jsonify({'status': 'success'})

@secretary_bp.route('/delete_notice/<int:notice_id>', methods=['POST'])
def delete_notice(notice_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Notice WHERE n_id = %s;', (notice_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True,'message': f'User {notice_id} deleted'})
    except Error as e:
        return jsonify({'success': False}), 500  


@secretary_bp.route('/issuenotice', methods=['POST','GET'])
def issuenotice():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['notice_title']
        content = request.form['notice_content']
        type = request.form['notice_type']
        print(title)
        try:
            connection = get_connection()
            cursor = connection.cursor()
            values = [session['sid'],title,content,type]
            cursor.execute("INSERT INTO Notice(sid,title,content,notice_type) VALUES(%s,%s,%s,%s)",values)
            connection.commit()
        except Error as e:
            print(f"An error occurred while inserting details: {e}", "danger")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        return redirect(url_for('dashboard'))
    
    return render_template('notice.html')

