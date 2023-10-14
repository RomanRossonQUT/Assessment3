from flask import Blueprint, jsonify, request
from soundscape import db

api_bp = Blueprint('api', __name__, url_prefix='/api')