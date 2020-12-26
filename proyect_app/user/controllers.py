from flask import Blueprint, render_template
from flask_user import login_required, current_user

from .models import User

userBp = Blueprint('user',__name__, url_prefix='/user')

@userBp.route('/')
def home():
    return render_template('user/home.html')

@userBp.route('/loginneed')
@login_required
def loginneed():
    print(current_user.id)
    print(current_user.username)
    return render_template('user/loginneed.html')
