from flask import Flask, request, render_template, Blueprint, session, url_for, redirect, flash
from mysql.connector import connect, Error
from database_connection import get_connection
from fetching_image import fetch_image_from_google_drive
import base64

flat_detail_bp = Blueprint('flat_details',__name__,url_prefix='/flat_details')

@flat_detail_bp.route('/',methods=['GET'])
def flat_details():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    connection = get_connection()
    if connection:
        try:
            flatno_query = "Select * from Flat_details where uid=%s;"
            value = (session['user_id'],)


            with connection.cursor() as cursor:
                cursor.execute(flatno_query,value)
                result = cursor.fetchone()    

        except Error as e:
            print(e)       
    else:
        print('Database connection failed')
    return render_template('flat_detail_page.html',flat = result)



