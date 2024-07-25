from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from mysql.connector import Error
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from mysql.connector import Error
from database_connection import get_connection
from fetching_image import fetch_image_from_google_drive
from data import user_data
import base64


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET','POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    photo_link = session.get('photo')
    image_data = fetch_image_from_google_drive(photo_link)

    # Encode image data to base64
    encoded_image = base64.b64encode(image_data).decode('utf-8') if image_data else None
    data = user_data(encoded_image, session['name'],session['s_name'])

    user = get_user()
    # print(user)
    form = EditProfileForm(obj=user)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users AS u JOIN society_detail AS s ON u.sid = s.sid JOIN flat_details AS f ON u.uid = f.uid WHERE u.uid = %s;",(session['user_id'],))
    data2 = cursor.fetchone()

    if session['role'] == 5:
        cursor.execute("SELECT * FROM users AS u JOIN society_detail AS s ON u.sid = s.sid WHERE u.uid = %s;",(session['user_id'],))
        data2 = cursor.fetchone()


    if request.method == 'POST':
        update_user(
            session['user_id'],
            form.uid.data,
            form.name.data,
            form.email.data,
            form.phone_no.data,
            form.flat_size.data
        )
        result = "Changes Saved"
        return redirect(url_for('dashboard',result=result))

    return render_template('profile_page.html', details=data, member_data=data2, form=form, user=user)

class EditProfileForm(FlaskForm):
    uid = StringField('uid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    flat_size = StringField('flat_size')
    phone_no = StringField('phone_no', validators=[
        DataRequired(), 
        Length(min=10, max=10, message="Phone number must be 10 digits"), 
        Regexp('^[0-9]*$', message="Phone number must contain only digits")
    ])
    submit = SubmitField('Save Changes')

def get_user():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users AS u JOIN flat_details AS f ON u.uid = f.uid WHERE u.uid = %s", (session['user_id'],))
    user = cursor.fetchone()

    if session['role'] == 5:
        cursor.execute("SELECT * FROM users WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def update_user(user_id, new_user_id, name, email, phone, flat_size):
    # print(user_id, new_user_id, name, email, phone, flat_size)
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Update the existing user record with the new UID
        update_q = '''UPDATE Users
                      SET uid = %s, name = %s, email = %s, phone = %s
                      WHERE uid = %s'''
        values = (new_user_id, name, email, phone, user_id)
        cursor.execute(update_q, values)

        update_q_2 = '''Update Flat_details set flat_size = %s where uid = %s'''
        cursor.execute(update_q_2,(flat_size,new_user_id))


        # Update session
        session['user_id'] = new_user_id
        session['name'] = name

        # Commit the transaction
        conn.commit()

    except Error as err:
        print(f"Database error: {err}")
        conn.rollback()  # Rollback in case of error

    except ValueError as ve:
        print(f"Value error: {ve}")
        conn.rollback()  # Rollback in case of error

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()


@profile_bp.route('/check_value', methods=['POST'])
def check_value():
    data = request.get_json()
    uid = data['values']['uid']
    if 'user_id' not in session or session['user_id'] != uid:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            userid_no_query = "SELECT COUNT(1) FROM Users WHERE uid = %s;"
            cursor.execute(userid_no_query, (uid,))
            uid_exists = cursor.fetchone()
        except Error as e:
            print(f"An error occurred while checking details: {e}")
            uid_exists = [0]  # Handle the error gracefully
        finally:
            cursor.close()
            connection.close()
    else:
        uid_exists = [0]  # No conflict if the same user
    
    return jsonify({
        'uidExists': uid_exists
    })
# Change Password
@profile_bp.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        current_password = request.form['password']
        new_password = request.form['newpassword']
        renew_password = request.form['renewpassword']
        

        user_id = session['user_id'] 
        db_connection = get_connection()
        cursor = db_connection.cursor()
        cursor.execute('SELECT password FROM login WHERE uid = %s', (user_id,))
        user = cursor.fetchone()
        
        
        if user and user[0]==current_password:
            if new_password == renew_password:
                cursor.execute('UPDATE login SET password = %s WHERE uid = %s', (new_password, user_id))
                db_connection.commit()
                result = 'Password changed successfully!'
                return redirect(url_for('dashboard', result=result))  # Redirect to profile page or wherever you want
            else:
                flash('New passwords do not match.', 'error')
        else:
            flash('Current password is incorrect.', 'error')
        
        cursor.close()
        db_connection.close()
    
    return redirect(url_for('dashboard'))

@profile_bp.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data['values']['password']
    connection = get_connection()
    cursor = connection.cursor()
    try:
        password_query = "Select password from Login where  uid =%s and password=%s;"
        cursor.execute(password_query,(session['user_id'],password))
        password_Equal = cursor.fetchone()
        if password_Equal is None:
            password_Equal = [0]
        # print(password_Equal)


    except Error as e:
        print(f"An error occurred while checking password: {e}", "danger")
     
    return jsonify({
        'passwordEqual': password_Equal
    })