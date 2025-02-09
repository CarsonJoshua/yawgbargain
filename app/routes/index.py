from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    # user = session.get('user')
    return render_template("index.html")
