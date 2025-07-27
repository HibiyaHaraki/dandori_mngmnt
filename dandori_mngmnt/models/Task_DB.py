
"""
Task_DB.py
SQLAlchemy model for the Task table in the Dandori Management database.

Created by Hibiya Haraki, May 2025.
"""

from dandori_mngmnt import db

# Task database model
class Task_DB(db.Model):
    """
    SQLAlchemy model for tasks.
    """
    __tablename__ = 'task'
    id              = db.Column(db.Integer     , primary_key = True )
    name            = db.Column(db.String( 255), nullable    = False)
    description     = db.Column(db.String( 511)                     )
    project         = db.Column(db.String( 511)                     )
    criteria        = db.Column(db.String( 511), nullable    = False)
    due_date        = db.Column(db.DateTime    , nullable    = False)
    status          = db.Column(db.String(  15), nullable    = False)
    assigned_by     = db.Column(db.String( 255), nullable    = False)
    comments        = db.Column(db.String( 511), nullable    = False)
    links           = db.Column(db.String( 511), nullable    = False)
