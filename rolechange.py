from flask import Flask, request, render_template
from mysql.connector import connect, Error

# Establish database connection
try:
    connection = connect(
        host="localhost",
        user="root",
        password="nmims@123",
        database="mysociety",
    )
except Error as e:
    print("Error:", e)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('update_role.html')

@app.route('/rolechange', methods=['POST'])
def rolechange():
    if request.method == 'POST':
        flat_no = request.form['flat_no']
        resident_name = request.form['name']
        old_role = request.form['old_role']
        new_role = request.form['new_role']

    
        print("Received data:", flat_no)  # Debugging line
        rolechange_db_query = "INSERT INTO update_roles (flat_no,name,old_role,new_role) VALUES (%s,%s,%s,%s);"
        values = (flat_no,resident_name,old_role,new_role)  # Correctly create a single-element tuple
       
        try:
            with connection.cursor() as cursor:
                cursor.execute(rolechange_db_query, values)  # Execute the query with parameters
                connection.commit()
                print("Data inserted successfully")
        except Error as e:
            print("Error:", e)  # Debugging line
            return render_template('error.html', error=str(e))  # Display error page
        return render_template('login.html')
    
if __name__ == '__main__':
    app.run(debug=1,port=9000)