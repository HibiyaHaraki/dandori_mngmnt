#
# May 2025. Created by Hibiya Haraki
#
# Response_Today_Step.py
#

from datetime import datetime, date, timedelta, time

from ...db  import db

from ...models.Step_DB     import Step_DB

from ...script.Step  import *
from ..Compare_Text  import compare_text
from ..Sound_Control import read_text

# Check similarity
def Check_Similrity_Today_Step(text):
    prompt = "What kind of action do I need to do?"
    threshold = 0.89

    if (compare_text(text,prompt,threshold=threshold)):
        return True
    else:
        return False


# Create Answer sentence
def Reply_Today_Step():
    # Get Steps
    filtered_steps_db_today = db.session.query(Step_DB) \
        .filter(Step_DB.due_date >= datetime.combine(date.today(), time()))\
        .filter(Step_DB.due_date <  datetime.combine(date.today(), time()) + timedelta(days=1))\
        .order_by(Step_DB.due_date)
    filtered_steps_db_past = db.session.query(Step_DB) \
        .filter(Step_DB.status != "DONE") \
        .filter(Step_DB.due_date < datetime.combine(date.today(), time()))\
        .order_by(Step_DB.due_date)
    to_do_steps = []
    if (filtered_steps_db_past.count() > 0):
        for step_db in filtered_steps_db_past:
            step = Step(step_db)
            to_do_steps.append(step)
    if (filtered_steps_db_today.count() > 0):
        for step_db in filtered_steps_db_today:
            step = Step(step_db)
            to_do_steps.append(step)

    for idx, step in enumerate(to_do_steps):
        read_text_str += "\n" + "Step No.{0} is {1}. You need to finish by {2}".format(idx+1,step.name,step.due_date.due_date)
    
    return read_text_str

# Answer Question
def Response_Today_Step(text):
    answer = Reply_Today_Step()
    read_text(answer)