#
# May 2025. Created by Hibiya Haraki
#
# Task_DB.py
#

from ..db import db

# Task database model
class Task_DB(db.Model):

    # Define Database
    __tablename__ = 'task'
    id              = db.Column(db.Integer     , primary_key = True )
    name            = db.Column(db.String( 255), nullable    = False)
    description     = db.Column(db.String( 511)                     )
    project         = db.Column(db.String( 511)                     )
    criteria        = db.Column(db.String( 511), nullable    = False)
    due_date        = db.Column(db.DateTime    , nullable    = False)
    status          = db.Column(db.String(  15), nullable    = False)
    steps           = db.Column(db.String( 511)                     )
    assigned_by     = db.Column(db.String( 255), nullable    = False)
    comments        = db.Column(db.String( 511), nullable    = False)
