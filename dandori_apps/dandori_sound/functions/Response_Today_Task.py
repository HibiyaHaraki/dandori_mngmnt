#
# May 2025. Created by Hibiya Haraki
#
# Response_Today_Step.py
#

from datetime import datetime, date, timedelta, time

from ...db  import db

from ...models.Task_DB     import Task_DB
from ...models.Step_DB     import Step_DB

from ...script.Task  import *
from ..Compare_Text  import compare_text
from ..Sound_Control import read_text

# Check similarity
def Check_Similrity_Today_Task(text):
    prompt = "What kind of task do I need to finish today?"
    threshold = 0.89

    if (compare_text(text,prompt,threshold=threshold)):
        return True
    else:
        return False

# Create Answer sentence
def Reply_Today_Step():
    # Get Steps
    filtered_tasks_db_today = db.session.query(Task_DB) \
        .filter(Task_DB.due_date >= datetime.combine(date.today(), time()))\
        .filter(Task_DB.due_date <  datetime.combine(date.today(), time()) + timedelta(days=1))\
        .order_by(Task_DB.due_date)
    filtered_tasks_db_past = db.session.query(Task_DB) \
        .filter(Task_DB.status != "DONE") \
        .filter(Task_DB.due_date < datetime.combine(date.today(), time()))\
        .order_by(Step_DB.due_date)
    to_do_tasks = []
    if (filtered_tasks_db_past.count() > 0):
        for task_db in filtered_tasks_db_past:
            task = Task(task_db)
            to_do_tasks.append(task)
    if (filtered_tasks_db_today.count() > 0):
        for task_db in filtered_tasks_db_today:
            task = Step(task_db)
            to_do_tasks.append(task)
            
    for idx, task in enumerate(to_do_tasks):
        read_text_str += "\n" + "Task No.{0} is {1}. You need to finish by {2}".format(idx+1,task.name,task.due_date.due_date)
    
    return read_text_str

# Answer Question
def Response_Today_Step(text):
    answer = Reply_Today_Step()
    read_text(answer)