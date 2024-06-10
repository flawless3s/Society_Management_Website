from flask import Flask, request, render_template
from mysql.connector import connect, Error

app = Flask(_name_)

@app.route('/')
def home():
    return render_template('security_form.html')


@app.route('/security_form', methods=['POST'])
def create():
    if request.method == 'POST':
        Security_ID = request.form['sec_id']
        Security_Password = request.form['security_password']
        
        
        print("Received data:", Security_ID, Security_Password)  # Debugging line
        try:
            with connect(
                host="localhost",
                user="root",
                password="nmims@123",
                database="mysociety",
            ) as connection: 
                create_db_query = "INSERT INTO security(sec_id,security_password) VALUES (%s,%s);"
                values = ( Security_ID, Security_Password)  # Correctly create a single-element tuple
                with connection.cursor() as cursor:
                    cursor.execute(create_db_query, values)  # Execute the query with parameters
                    connection.commit()  # Commit the transaction
                    print("Data inserted successfully")  # Debugging line

        except Error as e:
            print("Error:", e)  # Debugging line
            return render_template('error.html', error=str(e))  # Display error page

        return render_template('treasurerid.html')
    
if _name_ == '_main_':
    app.run(debug=True,port=9000)





    