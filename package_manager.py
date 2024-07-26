from flask import request, render_template, Blueprint,redirect, session, url_for, jsonify, flash
from mysql.connector import Error
from database_connection import get_connection
from data import fetch_package_data, fetch_package_advance

package_bp = Blueprint('package_manager',__name__,url_prefix='/package_manager')

@package_bp.route('/',methods=['GET'])
def package_manager():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    item = fetch_package_data()
    expected = fetch_package_advance()    
    return render_template('package_manager_page.html',items = item, packages_expected=expected)

@package_bp.route('/edit/<int:row_id>', methods=['GET', 'POST'])
def member_edit_row(row_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("Select * from MyGate_Resident where package_id=%s;", (row_id,))
    row = cursor.fetchone()
    # print(row)
    cursor.close()

    if request.method == 'POST':
        Package_Description = request.form['package_desc']
        Date_of_Arrival = request.form['date_arrival']
        Time_of_Arrival = request.form['time_arrival']
        Permission = 1 if request.form['permission'].lower() == 'true' else 0
        
        connection = get_connection()
        cursor = connection.cursor()
        values_tuple = (Package_Description, Date_of_Arrival, Time_of_Arrival, Permission, row_id)
        # print(values_tuple)
        cursor.execute("""
            UPDATE MyGate_Resident
            SET
                package_desc = %s,
                date_arrival = %s,
                time_arrival = %s,
                resident_permission = %s
            WHERE package_id = %s;""", values_tuple)
        connection.commit()
        cursor.close()
        result = "Permission Data Edited Successfully"


        return redirect(url_for('dashboard',result=result))

    return render_template('member_edit_row.html', row=row)


@package_bp.route('/member_delete_permission/<int:item_id>', methods=['POST'])
def member_delete_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM MyGate_Resident WHERE package_id = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success','success':True, 'message': f'Item {item_id} rejected'})
    except Error as e:
        error_message = f"Error deleting item {item_id}: {str(e)}"
        print(error_message)
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500


@package_bp.route('/advancepermission', methods=['POST','GET'])
def advancepermission():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        Package_Description = request.form['package_desc']
        Date_of_Arrival = request.form['date_arrival']
        Time_of_Arrival = request.form['time_arrival']
        Permission = 1 if request.form['permission'].lower() == 'true' else 0
        # print("Received data:", Package_Description,Date_of_Arrival,Time_of_Arrival,Permission)  # Debugging line
        
        connection = get_connection()
        
        if connection:
            try:
                package_insert_query = "INSERT INTO MyGate_Resident (Sid, Flat_No, Package_Desc, Date_Arrival, Time_Arrival, resident_permission) VALUES (%s, %s, %s, %s, %s, %s);"
                values = (session['sid'],session['flat_no'], Package_Description, Date_of_Arrival, Time_of_Arrival, Permission)
                cursor = connection.cursor()  # Corrected this line
                cursor.execute(package_insert_query, values)
                connection.commit()
                cursor.close()  
                result='Message Notified'
                return redirect(url_for("dashboard",result=result))


            except Error as e:
                print("Error:", e)  # Debugging line
                return render_template('error.html', error=str(e))  # Display error page
            
            finally:
                connection.close()

    return render_template('advancepermission.html')



@package_bp.route('/approve/<int:item_id>', methods=['POST'])
def approve_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE MyGate_Permission_Security SET permission = %s WHERE package_id = %s', ('1',item_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Item {item_id} approved'})
    except Error as e:
        return render_template('error.html',error=str(e))

@package_bp.route('/reject/<int:item_id>', methods=['POST'])
def reject_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE MyGate_permission_security SET permission = %s WHERE package_id = %s', ('2',item_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': f'Item {item_id} rejected'})
    except Error as e:
        return render_template('error.html',error=str(e))
    


@package_bp.route('/permissionrequired',methods=['GET','POST'])
def permissionrequired():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        Flat_No = request.form['flat_no']
        Package_Description = request.form['package_desc']
        Date_of_Arrival = request.form['date_arrival']
        Time_of_Arrival = request.form['time_arrival']

        connection = get_connection()
        
        if connection:
            try:
                package_insert_query = "INSERT INTO MyGate_Permission_Security (sid, Flat_No, Package_Desc, Time_Arrival, Date_Arrival) VALUES (%s, %s, %s, %s, %s);"
                values = (session['sid'],Flat_No, Package_Description, Time_of_Arrival, Date_of_Arrival)
                cursor = connection.cursor()  # Corrected this line
                cursor.execute(package_insert_query, values)
                connection.commit()
                cursor.close() 
                result = "Member Informed" 
                return redirect(url_for("dashboard",result=result))


            except Error as e:
                print("Error:", e)  # Debugging line
                return render_template('error.html', error=str(e))  # Display error page
            
            finally:
                connection.close()

    return render_template('permissionrequired.html')

@package_bp.route('/check_value', methods=['POST'])
def check_value():
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

@package_bp.route('/delete_permission/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM MyGate_Permission_Security WHERE package_id = %s', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success','success':True, 'message': f'Item {item_id} rejected'})
    except Error as e:
        error_message = f"Error deleting item {item_id}: {str(e)}"
        print(error_message)
        # Handle the error gracefully, you can render an error template or return a JSON response
        return jsonify({'status': 'error', 'message': error_message}), 500

@package_bp.route('/edit/<int:row_id>', methods=['GET', 'POST'])
def edit_row(row_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("Select * from MyGate_Permission_Security where package_id=%s;", (row_id,))
    row = cursor.fetchone()
    # print(row)
    cursor.close()

    if request.method == 'POST':
        flat_no = request.form['flat_no']
        package_desc = request.form['package_desc']
        date = request.form['date_arrival']
        time = request.form['time_arrival']
        
        connection = get_connection()
        cursor = connection.cursor()
        values_tuple = (flat_no, package_desc,date , time, row_id)
        # print(values_tuple)
        cursor.execute("""
            UPDATE MyGate_Permission_Security
            SET
                flat_no = %s,
                package_desc = %s,
                date_arrival = %s,
                time_arrival = %s
            WHERE package_id = %s;""", values_tuple)
        connection.commit()
        cursor.close()
        result = "Permission Data Edited Successfully"


        return redirect(url_for('dashboard',result=result))

    return render_template('security_edit_row.html', row=row)

    





    