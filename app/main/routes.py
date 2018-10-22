from flask import render_template, jsonify
from flask_security import login_required, roles_required, current_user
from app.main import bp


@bp.route('/')
@login_required
def index():
    return render_template('index.html')


@bp.route('/info')
@roles_required('admin')
def info():
    return jsonify(current_user.get_security_payload())

