from flask import Flask, request, render_template
from mysql.connector import connect, Error

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('treasurerid.html')


@app.route('/treasurerid', methods=['POST'])
def create():
    if request.method == 'POST':
        Treasurer_ID = request.form['treasurer_id']
        Treasurer_Password = request.form['treasurer_password']

    
        print("Received data:", Treasurer_ID, Treasurer_Password)  # Debugging line
        try:
            with connect(
                host="localhost",
                user="root",
                password="nmims@123",
                database="mysociety",
            ) as connection: 
                create_db_query = "INSERT INTO treasurer (treasurer_id,treasurer_password) VALUES (%s,%s);"
                values = (Treasurer_ID, Treasurer_Password)  # Correctly create a single-element tuple
                with connection.cursor() as cursor:
                    cursor.execute(create_db_query, values)  # Execute the query with parameters
                    connection.commit()  # Commit the transaction
                    print("Data inserted successfully")  # Debugging line

        except Error as e:
            print("Error:", e)  # Debugging line
            return render_template('error.html', error=str(e))  # Display error page

        return render_template('treasurerid.html')
    
if __name__ == '__main__':
    app.run(debug=True,port=9000)





    