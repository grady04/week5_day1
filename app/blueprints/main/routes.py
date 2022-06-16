from flask import render_template
from .import bp as main


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')