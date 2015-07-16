from flask import Blueprint

from unarea_science.service import SCIENCE_API

SCIENCE = Blueprint('science', __name__, url_prefix='/api/science')

SCIENCE_API.init_app(SCIENCE)
