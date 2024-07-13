from flask import Flask, request, render_template, Blueprint, session, url_for, redirect, flash
from mysql.connector import connect, Error
from fetching_image import fetch_image_from_google_drive
from data import user_data, fetch_maintenance_data
import base64

maintenance_bp = Blueprint('maintenance',__name__,url_prefix='/maintenance')


@maintenance_bp.route('/',methods=['GET'])
def maintenance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    photo_link = session.get('photo')
    image_data = fetch_image_from_google_drive(photo_link)

    if image_data:
        encoded_image = base64.b64encode(image_data).decode('utf-8')
    else:
        encoded_image = None
    data = user_data(encoded_image,session['name'])
    bill = fetch_maintenance_data()
    return render_template('maintenance.html',details = data, maintenance_bills = bill)