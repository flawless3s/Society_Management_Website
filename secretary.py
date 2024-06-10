from flask import Blueprint, request, render_template
from mysql.connector import Error 
from database_connection import get_connection

secretary_bp = Blueprint('secretary', __name__)

@secretary_bp.route('/document', methods=['POST'])
def secretary():
    if request.method == 'POST':
        Secretary_Id = request.form['sect_id']
        Secretary_Password = request.form['sect_password']

        print("Received data:", Secretary_Id, Secretary_Password)  # Debugging line
        connection = get_connection()
        if connection:
            try:
                secretary_db_query = "INSERT INTO secretary (sect_id,sect_password) VALUES (%s,%s);"
                values = (Secretary_Id, Secretary_Password)  # Correctly create a single-element tuple
                with connection.cursor() as cursor:
                    cursor.execute(secretary_db_query, values)  # Execute the query with parameters
                    connection.commit()
                    print("Data inserted successfully")    

            except Error as e:
                print("Error:", e)  # Debugging line
                return render_template('error.html', error=str(e))
            finally:
                connection.close()
        else:
            return render_template('error.html', error="Database connection failed")
    