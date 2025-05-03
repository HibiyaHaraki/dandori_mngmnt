#
# May 2025. Created by Hibiya Haraki
#
# __init__.py
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('dandori_mngmnt.config')

db = SQLAlchemy(app)
from .models.Step_DB    import Step_DB
from .models.Task_DB    import Task_DB
from .models.Comment_DB import Comment_DB

import dandori_mngmnt.dandori_mngmnt