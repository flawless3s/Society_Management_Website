from flask import Blueprint, request, render_template
from mysql.connector import Error
from database_connection import get_connection

create_bp = Blueprint('create', __name__, url_prefix='/create')

@create_bp.route('/', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        society_name = request.form['s_name']
        Society_Address = request.form['s_address']
        Society_id = request.form['sid']
        Area = request.form['area']
        City = request.form['city']
        State = request.form['state']
        Country = request.form['country']
        Secretary_Name = request.form['sect_name']
        Secretary_Number = request.form['sect_number']
        Total_Flats = request.form['total_flats']
        Empty_Flats = request.form['empty_flats']
        Total_Wings = request.form['total_wings']
        Total_Floor = request.form['total_floor']
        Flat_on_each_Floor = request.form['flat_on_each_floor']
        Builder_Name = request.form['build_name']
        Builder_Number = request.form['build_number']
        Company_Name = request.form['c_name']
        
        print("Received data:", society_name)

        create_db_query = """
        INSERT INTO NewGroup (s_name, s_address, sid, area, city, state, country, sect_name, sect_number, total_flats, empty_flat, total_wing, total_floor, no_of_flat_on_each_floor, build_name, build_no, c_name) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values = (
            society_name, Society_Address, Society_id, Area, City, State, Country, Secretary_Name, Secretary_Number, Total_Flats,
            Empty_Flats, Total_Wings, Total_Floor, Flat_on_each_Floor, Builder_Name, Builder_Number, Company_Name
        )
        
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(create_db_query, values) 
                    connection.commit()
                    print("Data inserted successfully")
                    connection.close()
                    return render_template('secretary_id.html')
            except Error as e:
                print("Error:", e)
                connection.close()
                return render_template('error.html', error=str(e))

        else:
            return render_template('error.html', error="Database connection failed")

    return render_template('create.html')
