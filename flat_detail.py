from flask import Flask, request, render_template, Blueprint, session, url_for, redirect, flash
from mysql.connector import connect, Error
from fetching_image import fetch_image_from_google_drive
from data import user_data, fetch_flat_data
import base64

flat_detail_bp = Blueprint('flat_details',__name__,url_prefix='/flat_details')

@flat_detail_bp.route('/',methods=['GET'])
def flat_details():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    photo_link = session.get('photo')
    if photo_link:
        image_data = fetch_image_from_google_drive(photo_link) 

        if image_data:
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            data = user_data(encoded_image,session['name'])
            flat_data = fetch_flat_data()
            print(flat_data)
        else:
            flash('Failed to fetch image data from Google Drive.')
            return redirect(url_for('login')) 
    else:
        flash('Photo link not found in session.')
        return redirect(url_for('login'))
    return render_template('flat_detail_page_(1).html',details = data,flat = flat_data)



