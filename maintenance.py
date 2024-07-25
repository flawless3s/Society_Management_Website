from flask import Flask, request, render_template, Blueprint, session, url_for, redirect, flash
from mysql.connector import connect, Error
from database_connection import get_connection

maintenance_bp = Blueprint('maintenance',__name__,url_prefix='/maintenance')


@maintenance_bp.route('/',methods=['GET'])
def maintenance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    connection = get_connection()
    if connection:
        try:
            Maintenance_query = "Select * from maintenance_display where uid=%s ;"
            value = (session['user_id'],)
            # print(session['user_id'])

            with connection.cursor() as cursor:
                cursor.execute(Maintenance_query,value)
                result = cursor.fetchall()
        except Error as e:
            return [('Could not fetch data')]        
    else:
        print('Database connection failed')
    return render_template('maintenance.html', maintenance_bills = result)