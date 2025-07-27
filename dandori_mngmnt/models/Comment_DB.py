
"""
Comment_DB.py
SQLAlchemy model for the Comment table in the Dandori Management database.

Created by Hibiya Haraki, May 2025.
"""

from datetime import datetime
from dandori_mngmnt import db

# Comment database model
class Comment_DB(db.Model):
    """
    SQLAlchemy model for comments.
    """
    __tablename__ = 'comment'
    id           = db.Column(db.Integer     , primary_key = True )
    created_date = db.Column(db.DateTime    , nullable=False     , default=datetime.now)
    updated_date = db.Column(db.DateTime    , nullable=False     , default=datetime.now, onupdate=datetime.now)
    comment      = db.Column(db.String( 511)                     )
