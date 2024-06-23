from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from mysql.connector import Error
from database_connection import get_connection

signup_bp = Blueprint('signup', __name__, url_prefix='/signup')

@signup_bp.route('/', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        pass

    return render_template('signup.html')
