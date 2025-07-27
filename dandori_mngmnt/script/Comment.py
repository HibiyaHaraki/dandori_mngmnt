
"""
Comment.py
Defines the Comment class and functions for handling comments in the Dandori Management system.

Created by Hibiya Haraki, May 2025.
"""

# Database model
from dandori_mngmnt import db
from dandori_mngmnt.models.Comment_DB import Comment_DB

# Required script
from dandori_mngmnt.script.Due_date   import STR_FORMAT

class Comment():
    """
    Class for handling comment objects and their updates.
    """
    def __init__(self, input=None):
        if input is None:
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

    def update(self, comment):
        """
        Update the comment text and commit to the database.
        """
        self.comment = comment
        updated_comment_db = Comment_DB(
            id      = self.id,
            comment = self.comment
        )
        db.session.merge(updated_comment_db)
        db.session.commit()

def add_new_comment(comment: str):
    """
    Add a new comment to the database.
    Args:
        comment (str): The comment text.
    Returns:
        int: The new comment's ID.
    """
    new_comment = Comment_DB(
        comment = comment
    )
    db.session.add(new_comment)
    db.session.commit()
    db.session.refresh(new_comment)
    return new_comment.id