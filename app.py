from flask import Flask, request, render_template, send_from_directory
from mysql.connector import Error
from database_connection import get_connection
from secretary import secretary_bp
from create import create_bp 


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        user_id = request.form['user_id']
        password = request.form['password']
        society_id = int(request.form['society_id'])
    
        connection = get_connection()
        if connection:
            try:
                login_db_query = "SELECT * FROM Login WHERE uid = %s and password = %s and sid = %s and role = %s;"
                values = (user_id,password,society_id,role)
                with connection.cursor() as cursor:
                    cursor.execute(login_db_query, values)
                    result = cursor.fetchall()
                    if len(result) == 1:
                        print("Login Successful!")
                        return render_template('index.html')
                    else:
                        return render_template('login_failed.html')
            except Error as e:
                print("Error:", e)
                return render_template('error.html', error=str(e))
            finally:
                connection.close()
        else:
            return render_template('error.html', error="Database connection failed")

    return render_template('login.html')


    
app.register_blueprint(secretary_bp)
app.register_blueprint(create_bp)
if __name__ == '__main__':
    app.run(debug=True, port=9000)
    
