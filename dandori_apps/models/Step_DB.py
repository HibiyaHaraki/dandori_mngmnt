#
# May 2025. Created by Hibiya Haraki
#
# Step_DB.py
#

from ..db import db

# Step database model
class Step_DB(db.Model):

    # Define Database
    __tablename__ = 'step'
    id              = db.Column(db.Integer     , primary_key = True )
    name            = db.Column(db.String( 255), nullable    = False)
    description     = db.Column(db.String( 511)                     )
    criteria        = db.Column(db.String( 511), nullable    = False)
    due_date        = db.Column(db.DateTime    , nullable    = False)
    status          = db.Column(db.String(  15), nullable    = False)
    parent_task     = db.Column(db.Integer     , nullable    = False)
    comments        = db.Column(db.String( 511), nullable    = False)