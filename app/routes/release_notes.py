from flask import Blueprint, render_template

release_notes_bp = Blueprint('index', __name__)

@release_notes_bp.route('/release_notes')
def release_notes():
    return render_template("release_notes.html")