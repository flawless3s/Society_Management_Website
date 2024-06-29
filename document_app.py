from flask import Flask, request, render_template, Blueprint, session, url_for, redirect, flash, send_file
from mysql.connector import connect, Error
from fetching_image import fetch_image_from_google_drive
from data import user_data,fetch_document_data
from database_connection import get_connection
import base64, io, mimetypes

document_bp = Blueprint('document',__name__,url_prefix='/document')

@document_bp.route('/',methods = ['GET'])
def document():
    if 'user_id' not in session:
      return  redirect (url_for('login'))
    photo_link = session.get('photo')
    if photo_link:
        image_data = fetch_image_from_google_drive(photo_link) 

        if image_data:
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            data = user_data(encoded_image,session['name'])
            document = fetch_document_data()
        else:
            flash('Failed to fetch image data from Google Drive.')
            return redirect(url_for('login')) 
    else:
        flash('Photo link not found in session.')
        return redirect(url_for('login'))
    return render_template('document_page2.html',details = data, items = document)

@document_bp.route('/document_form', methods=['POST','GET'])
def document_form():

    if request.method == 'POST':
        Document_Name = request.form['doc_name']
        file = request.files['file']

        print("Received data:", Document_Name, file.filename)  # Debugging line
        if file:
            file_data = file.read()
            # Convert file data to base64
            file_data_base64 = base64.b64encode(file_data)
        
            connection = get_connection()
        
            if connection:
                try:
                    package_insert_query = "INSERT INTO Documents (uid, doc_name, document_file) VALUES (%s, %s, %s);"
                    values = (session['user_id'], Document_Name, file_data_base64)
                    cursor = connection.cursor()  # Corrected this line
                    cursor.execute(package_insert_query, values)
                    connection.commit()
                    cursor.close() 
                    return redirect(url_for("document.document"))


                except Error as e:
                    print("Error:", e)  # Debugging line
                    return render_template('error.html', error=str(e))  # Display error page
            
                finally:
                    connection.close()
        else:
            return render_template('error.html', error="File could not be uploaded")  # Display error page

    return render_template('document.html')


@document_bp.route('/download/<int:file_id>',methods=['GET'])
def download(file_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT document_file, doc_name FROM Documents WHERE document_id = %s", (file_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        return 'File not found', 404

    file_data, file_name = result
    mime_type, _ = mimetypes.guess_type(file_name)
    mime_type = mime_type or 'application/octet-stream'

    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=file_name,
        mimetype=mime_type
    )


