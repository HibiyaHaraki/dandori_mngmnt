
"""
Due_date.py
Defines the Due_date class for handling due dates and their states in tasks.

Created by Hibiya Haraki, May 2025.
"""

from datetime import datetime

# JavaScript and display time formats
JS_TIME_FORMAT = '%Y-%m-%dT%H:%M'
STR_FORMAT = "%Y/%m/%d %H:%M"

class Due_date():
    """
    Class for handling due dates and their warning states.
    """
    def __init__(self, due_date: datetime, status: str = ''):
        self.due_date = due_date
        self.str_js   = self.due_date.strftime(JS_TIME_FORMAT)
        self.str      = self.due_date.strftime(STR_FORMAT)
        self.status   = status
        self.state    = ""
        td = due_date - datetime.now()
        if (status != 'DONE'):
            if (td.total_seconds() < 0):
                self.state = "due_date_danger"
            elif (td.days < 1):
                self.state = "due_date_warning"