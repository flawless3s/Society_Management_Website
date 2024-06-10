from flask import Flask, request, render_template
from mysql.connector import connect, Error

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('advancepermission.html')


@app.route('/advancepermission', methods=['POST'])
def create():
    if request.method == 'POST':
        Flat_No = request.form['flat_no']
        Package_Description = request.form['package_desc']
        Date_of_Arrival = request.form['date_arrival']
        Time_of_Arrival = request.form['time_arrival']
        Permission = request.form['permission']
        print("Received data:", Flat_No, Package_Description,Date_of_Arrival,Time_of_Arrival,Permission)  # Debugging line
        try:
            with connect(
                host="localhost",
                user="root",
                password="nmims@123",
                database="mysociety",
            ) as connection: 
                create_db_query = "INSERT INTO mygate_resident (flat_no,package_desc,date_arrival,time_arrival,permission) VALUES (%s,%s);"
                values = (Flat_No, Package_Description,Date_of_Arrival,Time_of_Arrival,Permission)  # Correctly create a single-element tuple
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





    