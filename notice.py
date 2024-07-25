from flask import Flask, request, jsonify, redirect, url_for, session, Blueprint
from mysql.connector import Error
from database_connection import get_connection

notice_bp = Blueprint('notice',__name__,url_prefix='/notice')

@notice_bp.route('/',methods=['GET'])
def notice():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    notices = []
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Notice where sid = %s ORDER BY post_date DESC LIMIT 5",(session['sid'],))
    notices = cursor.fetchall()
    cursor.close()
    conn.close()

    notice_list = []
    for notice in notices:
        notice_list.append({
            'id': notice[0],
            'title': notice[2],
            'content': notice[3],
            'type': notice[4],
            'date': notice[5]
        })
    return jsonify(notice_list)


