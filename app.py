from flask import Flask, request, render_template, redirect, url_for, flash, session
from mysql.connector import Error
from database_connection import get_connection
from drive_link_conversion import convert_drive_link
from fetching_image import fetch_image_from_google_drive
from secretary import secretary_bp
from signup import signup_bp
from notice import notice_bp
from maintenance import maintenance_bp
from package_manager import package_bp
from document_app import document_bp
from flat_detail import flat_detail_bp
from profile_page import profile_bp
from admin import admin_bp
from treasurer_app import treasurer_bp
from data import user_data,fetch_package_permission,fetch_package_advance
from datetime import timedelta
import os
import base64


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user_id = request.form['user_id']
        password = request.form['password']

        connection = get_connection()
        
        if connection:
            try:
                login_db_query = "SELECT * FROM login WHERE uid = %s and password = %s;"
                values = (user_id, password)
                
                with connection.cursor() as cursor:
                    cursor.execute(login_db_query, values)
                    login_result = cursor.fetchone()
                    
                    
                    if login_result:
                        session_db_query = "SELECT * FROM users where uid = %s;"
                        values = (user_id,)

                        cursor.execute(session_db_query, values)
                        session_result = cursor.fetchone()
                        

                        session['user_id'] = session_result[2]
                        session['role'] = session_result[1]
                        session['name'] = session_result[3]
                        session['sid'] = session_result[0]
                        session['approval'] = session_result[7]
                        session['is_active'] = session_result[10]
                        direct_photo_link = session_result[6]

                        if direct_photo_link:
                            session['photo'] = convert_drive_link(direct_photo_link)

                        if session['role'] != 1: 
                            session_db_query_2 = "SELECT s_name FROM Society_detail where sid = %s;"
                            cursor.execute(session_db_query_2, (session['sid'],))
                            session_result_2 = cursor.fetchone()
                            session['s_name'] = session_result_2[0] 
                        else:
                            session['s_name'] = None 

                        if session['role'] != 5 and session['role'] != 1:
                            session_db_query_3 = "SELECT flat_no From Flat_Details where uid=%s and sid = %s;"
                            cursor.execute(session_db_query_3, (session['user_id'],session['sid']))
                            session_result_3 = cursor.fetchone()
                            session['flat_no'] = session_result_3[0]                    


                        return redirect(url_for('dashboard'))
                    else:
                        flash('Login failed. Please check your credentials and try again.')
            except Error as e:
                print("Error:", e)
                return render_template('error.html', error=str(e))
            finally:
                connection.close()
        else:
            return render_template('error.html', error="Database connection failed")
        
    return render_template('login.html')


@app.route('/dashboard', methods =['GET','POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Session has expired, Please login again.")
        return redirect(url_for('login'))
    if not session['approval'] or not session['is_active']:
        return render_template('waiting_page.html')
    

    role = session['role']
    user_name = session['name']
    photo_link = session.get('photo')

    # if photo_link:
    image_data = fetch_image_from_google_drive(photo_link)

    # Encode image data to base64
    if image_data:
        encoded_image = base64.b64encode(image_data).decode('utf-8')
    else:
        encoded_image = None
    data = user_data(encoded_image,user_name, session['s_name'])
    #  else:
    #     flash('Failed to fetch image data from Google Drive.')
    #     return redirect(url_for('login'))
    result = request.args.get('result', None)
    if role == 1:
        return render_template('admin_dashboard.html', details = data,result='')
    elif role == 2:
        return render_template('Secretary_dashboard.html', details = data,result=result)
    elif role == 3:
        return render_template('Treasurer_dashboard.html', details = data, result=result)
    elif role == 4:
        # bill = fetch_mantenance_data()
        return render_template('Member_dashboard.html', details = data, result=result)
    elif role == 5:
        permission,expected = fetch_package_permission(), fetch_package_advance()
        print(permission)
        return render_template('Security_Dashboard.html', details = data, package_permissions = permission, packages_expected = expected,result=result)
    # else:
    #     flash('Photo link not found in session.')
    #     return redirect(url_for('login'))

app.register_blueprint(signup_bp)  
app.register_blueprint(secretary_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(package_bp)
app.register_blueprint(document_bp)
app.register_blueprint(flat_detail_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(treasurer_bp)

@app.route('/logout')
def logout():
    session.clear()
    flash('You were successfully logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=9000)
    
