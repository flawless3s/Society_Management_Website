from flask import Flask, request, render_template, redirect, url_for, flash, session
from mysql.connector import Error
from database_connection import get_connection
from drive_link_conversion import convert_drive_link
from fetching_image import fetch_image_from_google_drive
from secretary import secretary_bp
from create import create_bp
from signup import signup_bp
from data import user_data,fetch_maintenance_data
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

        role = int(request.form['role'])
        user_id = request.form['user_id']
        password = request.form['password']

        connection = get_connection()
        if connection:
            try:
                login_db_query = "SELECT * FROM login WHERE uid = %s and password = %s and role_id = %s;"
                values = (user_id, password, role)
                
                with connection.cursor() as cursor:
                    cursor.execute(login_db_query, values)
                    login_result = cursor.fetchone()
                    
                    if login_result:
                        session_db_query = "SELECT * FROM users where uid = %s and password = %s and role_id = %s;"
                        values = (user_id,password, role)

                        cursor.execute(session_db_query, values)
                        session_result = cursor.fetchone()

                        session['user_id'] = session_result[2]
                        session['role'] = session_result[1]
                        session['name'] = session_result[4]
                        direct_photo_link = session_result[7]

                       
                        session['photo'] = convert_drive_link(direct_photo_link)


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


@app.route('/dashboard', methods =['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    user_name = session['name']
    photo_link = session.get('photo')

    if photo_link:
        image_data = fetch_image_from_google_drive(photo_link)

        # Encode image data to base64
        if image_data:
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            data = user_data(encoded_image,user_name)
        else:
            flash('Failed to fetch image data from Google Drive.')
            return redirect(url_for('login'))

        if role == 1:
            return render_template('dashboard.html', details = data)
        elif role == 2:
            return render_template('Secretary_dashboard.html', details = data)
        elif role == 3:
            return render_template('Treasurer_dashboard.html', details = data)
        elif role == 4:
            bill = fetch_maintenance_data()
            print(bill)
            return render_template('Member_dashboard.html', details = data, maintenance_bills = bill)
        elif role == 5:
            return render_template('Security_dashboard.html', details = data)
    else:
        flash('Photo link not found in session.')
        return redirect(url_for('login'))

app.register_blueprint(signup_bp)  
app.register_blueprint(secretary_bp)
app.register_blueprint(create_bp)

@app.route('/logout')
def logout():
    session.clear()
    flash('You were successfully logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=9000)
    
