from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from mysql.connector import Error
from database_connection import get_connection
from fetching_image import fetch_image_from_google_drive
from data import user_data
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io



# SCOPES = ['https://www.googleapis.com/auth/drive.file']
# SERVICE_ACCOUNT_FILE = 'path_to_your_service_account_file.json'

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# drive_service = build('drive', 'v3', credentials=credentials)


profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET','POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    photo_link = session.get('photo')
    image_data = fetch_image_from_google_drive(photo_link)

    # Encode image data to base64
    encoded_image = base64.b64encode(image_data).decode('utf-8') if image_data else None
    data = user_data(encoded_image, session['name'])

    user = get_user()
    print(user)
    form = EditProfileForm(obj=user)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users AS u JOIN society_detail AS s ON u.sid = s.sid JOIN flat_details AS f ON u.uid = f.uid WHERE u.uid = %s;",(session['user_id'],))
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
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('profile_page.html', details=data, member_data=data2, form=form, user=user)

class EditProfileForm(FlaskForm):
    uid = StringField('uid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    flat_size = StringField('flat_size', validators=[DataRequired()])
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
    cursor.close()
    conn.close()
    return user

def update_user(user_id, new_user_id, name, email, phone, flat_size):
    print(user_id, new_user_id, name, email, phone, flat_size)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Update users table
        cursor.execute(
            "UPDATE users SET uid = %s, name = %s, email = %s, phone = %s WHERE uid = %s",
            (new_user_id, name, email, phone, user_id)
        )
        cursor.execute(
            "UPDATE Login SET uid = %s WHERE uid = %s",
            (new_user_id, user_id)
        )

        # Update flat_details table
        if session['role'] != 5: 
            cursor.execute(
                "UPDATE flat_details SET flat_size = %s, uid = %s WHERE uid = %s",
                (flat_size, new_user_id, user_id)
            )

            cursor.execute(
                "UPDATE Documents SET uid = %s WHERE uid = %s",
                (new_user_id, user_id)
            )

            cursor.execute(
                "UPDATE Maintenance_display SET uid = %s WHERE uid = %s",
                (new_user_id, user_id)
            )

        session['user_id'] = new_user_id
        session['name'] = name
        # Commit the transaction
        conn.commit()
        
    except Error as err:
        print(f"Error: {err}")
        conn.rollback()  # Rollback in case of error

    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()


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
        print(user)
        
        if user and user[0]==current_password:
            if new_password == renew_password:
                cursor.execute('UPDATE login SET password = %s WHERE uid = %s', (new_password, user_id))
                db_connection.commit()
                flash('Password changed successfully!', 'success')
                return redirect(url_for('dashboard'))  # Redirect to profile page or wherever you want
            else:
                flash('New passwords do not match.', 'error')
        else:
            flash('Current password is incorrect.', 'error')
        
        cursor.close()
        db_connection.close()
    
    return redirect(url_for('dashboard'))

