#
# May 2025. Created by Hibiya Haraki
#
# Comment_DB.py
#

from datetime import datetime
from ..db import db

# Commnet database model
class Comment_DB(db.Model):

    # Define Database
    __tablename__ = 'comment'
    id           = db.Column(db.Integer     , primary_key = True )
    created_date = db.Column(db.DateTime    , nullable=False     , default=datetime.now)
    updated_date = db.Column(db.DateTime    , nullable=False     , default=datetime.now, onupdate=datetime.now)
    comment      = db.Column(db.String( 511)                     )
