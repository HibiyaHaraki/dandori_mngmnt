#
# May 2025. Created by Hibiya Haraki
#
# Comment.py
#

import json
from datetime import datetime

# Database model
from ..db import db
from ..models.Comment_DB import Comment_DB

# Required script
from .Due_date   import STR_FORMAT

# Comment class definition
class Comment():

    # Constructor
    def __init__(self, input = None):
        if (input == None):
            pass
        elif (type(input) is int):
            if (input <= db.session.query(Comment_DB).count()):
                comment_db = db.session.query(Comment_DB).get(input)
            else:
                pass
        elif (type(input) is Comment_DB):
            comment_db = input
        
        self.id           = comment_db.id
        self.created_date = comment_db.created_date
        self.updated_date = comment_db.updated_date
        self.comment      = comment_db.comment

        self.created_date_str = self.created_date.strftime(STR_FORMAT)
        self.updated_date_str = self.updated_date.strftime(STR_FORMAT)
    
    def update(self,comment):
        self.comment = comment
        updated_comment_db = Comment_DB(
            id      = self.id,
            comment = self.comment
        )
        db.session.merge(updated_comment_db)
        db.session.commit()

# Add new comment
def add_new_comment(
    comment:str
):
    new_comment = Comment_DB(
        comment = comment
    )
    db.session.add(new_comment)
    db.session.commit()
    db.session.refresh(new_comment)
    return new_comment.id