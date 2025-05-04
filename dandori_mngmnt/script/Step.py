#
# May 2025. Created by Hibiya Haraki
#
# Step.py
#

import json
from datetime import datetime, timedelta, time

# Database model
from dandori_mngmnt import db
from dandori_mngmnt.models.Step_DB import Step_DB

# Required script
from dandori_mngmnt.script.Due_date import Due_date, JS_TIME_FORMAT
from dandori_mngmnt.script.Status   import Status, STATUS_LIST, ALL_STATUS
from dandori_mngmnt.script.Comment  import Comment


# Step class definition
class Step():

    # Constructor
    def __init__(self, input = None):
        if (input == None):
            pass
        elif (type(input) is int):
            if (input <= db.session.query(Step_DB).count()):
                step_db = db.session.query(Step_DB).get(input)
            else:
                pass
        elif (type(input) is Step_DB):
            step_db = input

        self.id           = step_db.id
        self.sysID        = "STEP/" + str(self.id)
        self.name         = step_db.name
        self.description  = step_db.description
        self.criteria     = step_db.criteria
        self.due_date     = Due_date(step_db.due_date,status=step_db.status)
        self.status       = Status(step_db.status)
        self.url          = "/" + self.sysID
        self.parent_task = step_db.parent_task
        self.comments     = json.loads(step_db.comments)
    
    def update(self):
        new_step_db = Step_DB(
            id           = self.id,
            name         = self.name,
            description  = self.description,
            criteria     = self.criteria,
            due_date     = self.due_date.due_date,
            status       = self.status.state_str,
            parent_task = self.parent_task,
            comments     = json.dumps(self.comments)
        )
        db.session.merge(new_step_db)
        db.session.commit()
    
    def get_comments(self):
        comments = []
        for commentID in self.comments:
            comments.append(Comment(commentID))
        return comments

# Check input
def check_step_input(
    form_name:str,
    form_str_due_date:str,
    form_criteria:str,
    parent_taskID:int,
    form_description:str = ''
):
    invalid_input_flag = False
    invalid_inputs = []
    # Check input Step Name
    if (len(form_name) < 1):
        invalid_input_flag = True
        invalid_inputs.append('Step Name')
    
    # Check input criteria  
    if (len(form_criteria) < 1):
        invalid_input_flag = True
        invalid_inputs.append('Criteria')
    
    # Check input due date
    if (len(form_str_due_date) < 1):
        invalid_input_flag = True
        invalid_inputs.append('Due Date')
    else:
        try:
            form_datetime_due_date = datetime.strptime(form_str_due_date, JS_TIME_FORMAT)
        except:
            invalid_input_flag = True
            invalid_inputs.append('Due Date Format')
    
    return invalid_input_flag, invalid_inputs
    

# Add new step
def add_new_Step(
    form_name:str,
    form_str_due_date:str,
    form_criteria:str,
    parent_taskID:int,
    form_description:str = ''
):
    # Check input
    invalid_input_flag, invalid_inputs = check_step_input(
        form_name,
        form_str_due_date,
        form_criteria,
        parent_taskID,
        form_description
    )
    
    # Error input
    if (invalid_input_flag):
        return invalid_input_flag, invalid_inputs, None
    form_datetime_due_date = datetime.strptime(form_str_due_date, JS_TIME_FORMAT)
    
    # Create new Step data
    step_status = Status()
    new_step = Step_DB(
        name         = form_name,
        description  = form_description,
        criteria     = form_criteria,
        due_date     = form_datetime_due_date,
        status       = step_status.state_str,
        parent_task  = parent_taskID,
        comments     = json.dumps([])
    )
    return invalid_input_flag, invalid_inputs, new_step

def _get_new_stepID():
    return db.session.query(Step_DB).count() + 1

def get_new_stepID():
    return "STEP/" + str(_get_new_stepID())

# Function for analysis
def get_Step_DB_by_query(
    statuses:list           = ALL_STATUS,
    start_due_date:datetime = None,
    end_due_date:datetime   = None
):
    if (start_due_date is not None and end_due_date is not None):
        if (start_due_date > end_due_date):
            return None
    
    Step_DB_list = db.session.query(Step_DB)

    # Filter by Status
    if (len(statuses) > 0):
        Step_DB_list = Step_DB_list.filter(Step_DB.status.in_(statuses))
    
    # Filter by due_date
    if (start_due_date != None):
        Step_DB_list = Step_DB_list.filter(Step_DB.due_date >= start_due_date)
    if (end_due_date != None):
        Step_DB_list = Step_DB_list.filter(Step_DB.due_date <  end_due_date)

    return Step_DB_list

def get_step_status_analysis_data(
    statuses:list = ALL_STATUS, 
    start_due_date:datetime = None, 
    end_due_date:datetime = None
):
    # Get source step db list
    Step_DB_list = get_Step_DB_by_query(
        statuses, start_due_date, end_due_date
    )

    # Get step status statistics for graph
    status_statistics = {
        'labels' : [],
        'data'   : [],
        'color'  : [],
        'index'  : []
    }
    
    for idx, status in enumerate(statuses):
        for status_info in STATUS_LIST.keys():
            if (status == STATUS_LIST[status_info]['str']):
                status_statistics['labels'].append(status)
                status_statistics['color' ].append(STATUS_LIST[status_info]['color'])
                status_statistics['index' ].append(idx)
                status_statistics['data'  ].append(
                    Step_DB_list\
                        .filter(Step_DB.status == status)\
                        .count()
                )
                break

    return status_statistics

def get_step_dueDate_analysis_data(
    statuses:list = ALL_STATUS, 
    start_due_date:datetime = None, 
    end_due_date:datetime = None
):
    # Get source step db list
    Step_DB_list = get_Step_DB_by_query(
        statuses, start_due_date, end_due_date
    )

    dueDate_statistics = {
        'labels' : [],
        'data'   : {},
        'color'  : []
    }

    if (Step_DB_list.count() > 0):
        start_time_db = Step_DB_list.order_by(Step_DB.due_date).first()
        start_time    = Step(start_time_db).due_date.due_date
        end_time_db   = Step_DB_list.order_by(Step_DB.due_date.desc()).first()
        end_time      = Step(end_time_db).due_date.due_date
        date_list = []
        day = 0
        while(datetime.combine(start_time, time()) + timedelta(days=day) <= end_time):
            date_list.append(start_time + timedelta(days=day))
            dueDate_statistics['labels'].append((start_time + timedelta(days=day)).strftime('%Y/%m/%d'))
            day += 1

        # Get step status statistics for graph
        for status in statuses:
            for status_info in STATUS_LIST.keys():
                if (status == STATUS_LIST[status_info]['str']):
                    dueDate_statistics['data'][status] = []
                    dueDate_statistics['color'].append(STATUS_LIST[status_info]['color'])
                    for start_date in date_list:
                        temp_start_time = datetime.combine(start_date, time())
                        temp_end_time = datetime.combine(start_date + timedelta(days=1), time())
                        dueDate_statistics['data'][STATUS_LIST[status_info]['str']].append(
                            Step_DB_list\
                                .filter(Step_DB.status   == status)\
                                .filter(Step_DB.due_date >= temp_start_time)\
                                .filter(Step_DB.due_date <  temp_end_time)\
                                .count()
                        )
    
    return dueDate_statistics