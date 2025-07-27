
"""
__init__.py
Initializes the Flask app and SQLAlchemy database for the Dandori Management system.

Created by Hibiya Haraki, May 2025.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create Flask app and load configuration
app = Flask(__name__)
app.config.from_object('dandori_mngmnt.config')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import database models to register them with SQLAlchemy
from .models.Task_DB import Task_DB
from .models.Comment_DB import Comment_DB

# Import main application logic
import dandori_mngmnt.dandori_mngmnt