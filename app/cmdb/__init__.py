from flask import Blueprint

bp = Blueprint('cmdb', __name__)

from app.cmdb import routes
