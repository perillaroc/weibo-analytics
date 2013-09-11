# encoding: utf-8
from flask import Blueprint, request, url_for, render_template, jsonify

api_app = Blueprint('api_app', __name__,template_folder='templates')

from myapp.api_app import api_user_view