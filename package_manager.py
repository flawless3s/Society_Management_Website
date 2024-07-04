from flask import Flask, request, render_template, Blueprint,redirect, session, url_for, jsonify, flash
from mysql.connector import connect, Error
from database_connection import get_connection
from fetching_image import fetch_image_from_google_drive
from data import fetch_package_data,user_data
import base64

package_bp = Blueprint('package_manager',__name__,url_prefix='/package_manager')

@package_bp.route('/',methods=['GET'])
def package_manager():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    item = fetch_package_data()
    photo_link = session.get('photo')
    if photo_link:
        image_data = fetch_image_from_google_drive(photo_link) 

        if image_data:
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            data = user_data(encoded_image,session['name'])
        else:
            flash('Failed to fetch image data from Google Drive.')
            return redirect(url_for('login')) 
    else:
        flash('Photo link not found in session.')
        return redirect(url_for('login'))
     
    return render_template('package_manager_page.html',items = item,details = data)



@package_bp.route('/advancepermission', methods=['POST','GET'])
def advancepermission():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        print("Hello")
        Flat_No = request.form['flat_no']
        Package_Description = request.form['package_desc']
        Date_of_Arrival = request.form['date_arrival']
        Time_of_Arrival = request.form['time_arrival']
        Permission = 1 if request.form['permission'].lower() == 'true' else 0
        print("Received data:", Flat_No, Package_Description,Date_of_Arrival,Time_of_Arrival,Permission)  # Debugging line
        
        connection = get_connection()
        
        if connection:
            try:
                package_insert_query = "INSERT INTO MyGate_Resident (Sid, Flat_No, Package_Desc, Date_Arrival, Time_Arrival, resident_permission) VALUES (%s, %s, %s, %s, %s, %s);"
                values = (session['sid'],Flat_No, Package_Description, Date_of_Arrival, Time_of_Arrival, Permission)
                cursor = connection.cursor()  # Corrected this line
                cursor.execute(package_insert_query, values)
                connection.commit()
                cursor.close()  
                return redirect(url_for("dashboard"))


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
        cursor.execute('UPDATE MyGate_Permission_Security SET permission = %s WHERE package_id = %s', (1,item_id))
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
        cursor.execute('UPDATE MyGate_permission_security SET permission = %s WHERE package_id = %s', (0,item_id))
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
        print("Hello")
        Flat_No = request.form['flat_no']
        Package_Description = request.form['package_desc']
        Date_of_Arrival = request.form['date_arrival']
        Time_of_Arrival = request.form['time_arrival']

        print("Received data:", Flat_No, Package_Description,Date_of_Arrival,Time_of_Arrival)  # Debugging line
        
        connection = get_connection()
        
        if connection:
            try:
                package_insert_query = "INSERT INTO MyGate_Permission_Security (sid, Flat_No, Package_Desc, Time_Arrival, Date_Arrival) VALUES (%s, %s, %s, %s, %s);"
                values = (session['sid'],Flat_No, Package_Description, Time_of_Arrival, Date_of_Arrival)
                cursor = connection.cursor()  # Corrected this line
                cursor.execute(package_insert_query, values)
                connection.commit()
                cursor.close()  
                return redirect(url_for("dashboard"))


            except Error as e:
                print("Error:", e)  # Debugging line
                return render_template('error.html', error=str(e))  # Display error page
            
            finally:
                connection.close()

    return render_template('permissionrequired.html')



    





    