from flask import Flask, request, render_template
from mysql.connector import connect, Error

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('document.html')

@app.route('/document', methods=['POST'])
def create():
    if request.method == 'POST':
        Document_Id = request.form['doc_id']
        Document_Name = request.form['doc_name']
        Document_Type = request.form['doc_type']
        file = request.files['file']  # Use request.files to get the file

        if file:
            file_content = file.read()  # Read the file content

            print("Received data:", Document_Id, Document_Name, Document_Type, file.filename)  # Debugging line

            try:
                with connect(
                    host="localhost",
                    user="root",
                    password="nmims@123",
                    database="mysociety",
                ) as connection:
                    create_db_query = "INSERT INTO Documents (document_id, doc_name, document_type, document_file) VALUES (%s, %s, %s, %s);"
                    values = (Document_Id, Document_Name, Document_Type, file_content)
                    with connection.cursor() as cursor:
                        cursor.execute(create_db_query, values)  # Execute the query with parameters
                        connection.commit()  # Commit the transaction
                        print("Data inserted successfully")  # Debugging line

            except Error as e:
                print("Error:", e)  # Debugging line
                return render_template('error.html', error=str(e))  # Display error page

        return render_template('treasurerid.html')

if __name__ == '__main__':
    app.run(debug=True, port=9000)
