import datetime
from database_connection import get_connection

def check_time():
    twenty_four_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=24)


    update_query = """
        UPDATE MyGate_Permission_Security
        SET permission = '2'
        WHERE date_arrival <= %s
        AND time_arrival <= %s
        AND permission != '2'
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(update_query, (twenty_four_hours_ago.date(), twenty_four_hours_ago.time()))


    connection.commit()

    cursor.close()
    connection.close()
