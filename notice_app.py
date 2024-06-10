from flask import Flask, request, render_template
from mysql.connector import connect, Error

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('notice.html')


@app.route('/notice', methods=['POST'])
def create():
    if request.method == 'POST':
        Notice_ID = request.form['notice_id']
        Notice_Title = request.form['notice_title']
        Notice_Content = request.form['notice_content']
        Date=request.form['date']
       
       
        print("Received data:", Notice_ID, Notice_Title,Notice_Content,Date)  # Debugging line
        try:
            with connect(
                host="localhost",
                user="root",
                password="nmims@123",
                database="mysociety",
            ) as connection: 
                create_db_query = "INSERT INTO notice (n_id,title, content,post_date) VALUES (%s,%s,%s,%s);"
                values = (Notice_ID, Notice_Title,Notice_Content,Date)  # Correctly create a single-element tuple
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
