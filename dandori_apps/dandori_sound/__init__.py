#
# May 2025. Created by Hibiya Haraki
#
# __init__.py
#

import os
from flask import Flask

from ..db import db, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dandori_mngmnt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
init_db(app)

from ..models.Step_DB    import Step_DB
from ..models.Task_DB    import Task_DB
from ..models.Comment_DB import Comment_DB

import dandori_apps.dandori_sound.dandori_sound

def start_dandori_sound():
    if (not os.path.isfile('instance/dandori_mngmnt.db')):
        with app.app_context():
            db.create_all()
    app.run(port=5001)