#
# May 2025. Created by Hibiya Haraki
#
# Task.py
#

import json
from datetime import datetime, timedelta, time

# Database model
from dandori_mngmnt import db
from dandori_mngmnt.models.Task_DB import Task_DB

# Required script
from dandori_mngmnt.script.Due_date import Due_date, JS_TIME_FORMAT
from dandori_mngmnt.script.Status   import Status, STATUS_LIST, ALL_STATUS
from dandori_mngmnt.script.Comment  import Comment
from dandori_mngmnt.script.Links    import generate_mermaid_command, get_relationship_list, get_pair_relationship

# Task class definition
class Task():

    # Constructor
    def __init__(self, input = None):
        if input == None:
            pass
        elif (type(input) is int):
            if (input <= db.session.query(Task_DB).count()):
                task_db = db.session.query(Task_DB).get(input)
            else:
                pass
        elif (type(input) is Task_DB):
            task_db = input
        
        self.id                 = task_db.id
        self.sysID              = "TASK/" + str(self.id)
        self.name               = task_db.name
        self.description        = task_db.description
        self.project            = task_db.project
        self.criteria           = task_db.criteria
        self.due_date           = Due_date(task_db.due_date,status=task_db.status)
        self.status             = Status(task_db.status)
        self.assigned_by        = task_db.assigned_by
        self.url                = "/" + self.sysID
        self.comments           = json.loads(task_db.comments)
        self.links              = json.loads(task_db.links)
    
    # Update database data of Task
    def update(self):
        updated_task_db = Task_DB(
            id          = self.id,
            name        = self.name,
            description = self.description,
            project     = self.project,
            criteria    = self.criteria,
            due_date    = self.due_date.due_date,
            status      = self.status.state_str,
            assigned_by = self.assigned_by,
            comments    = json.dumps(self.comments),
            links       = json.dumps(self.links)
        )
        db.session.merge(updated_task_db)
        db.session.commit()

    def get_comments(self):
        comments = []
        for commentID in self.comments:
            comments.append(Comment(commentID))
        return comments
    
    def _mermaid_command_input(self):
        mermaid_input = []

        for link in self.links:
            input_command = {
                "TargetTaskID": link["TaskID"],
                "relationship": link["relationship"],
                "SourceTaskID": self.id,
                "TargetStatus": Task(int(link["TaskID"])).status.state_str,
                "SourceStatus": self.status.state_str
            }
            mermaid_input.append(input_command)
        
        return mermaid_input

    def get_mermaid_command(self):
        mermaid_command_input = self._mermaid_command_input()
        mermaid_command = generate_mermaid_command(mermaid_command_input)
        return mermaid_command


# Check input
def check_task_input(
    form_name:str,
    form_str_due_date:str,
    form_criteria:str,
    form_assignedby:str,
    form_project:str = '',
    form_description:str = ''
):
    invalid_input_flag = False
    invalid_inputs = []
    # Check input Task Name
    if (len(form_name) < 1):
        invalid_input_flag = True
        invalid_inputs.append('Task Name')
    
    # Check input Task Assigned By
    if (len(form_assignedby) < 1):
        invalid_input_flag = True
        invalid_inputs.append('Assigned By')
    
    # Check input Task Due Date
    if (len(form_str_due_date) < 1):
        invalid_input_flag = True
        invalid_inputs.append('Due Date')
    else:
        try:
            form_datetime_due_date = datetime.strptime(form_str_due_date, JS_TIME_FORMAT)
        except:
            invalid_input_flag = True
            invalid_inputs.append('Due Date Format')
    
    # Check input Task Criteria
    if (len(form_criteria) < 1):
        criteria_invalid_flag = True
        invalid_inputs.append('Criteria')
    
    return invalid_input_flag, invalid_inputs

# Add new task
def add_new_Task(
    form_name:str,
    form_str_due_date:str,
    form_criteria:str,
    form_assignedby:str,
    form_project:str = '',
    form_description:str = ''
):
    
    invalid_input_flag, invalid_inputs = check_task_input(
        form_name,
        form_str_due_date,
        form_criteria,
        form_assignedby,
        form_project,
        form_description
    )

    if (invalid_input_flag):
        return invalid_input_flag, invalid_inputs, None
    form_datetime_due_date = datetime.strptime(form_str_due_date, JS_TIME_FORMAT)
    
    # Create new Task data
    new_task_status = Status()
    new_task = Task_DB(
        name        = form_name,
        description = form_description,
        project     = form_project,
        criteria    = form_criteria,
        due_date    = form_datetime_due_date,
        status      = new_task_status.state_str,
        assigned_by = form_assignedby,
        comments    = json.dumps([]),
        links       = json.dumps([])
    )
    return invalid_input_flag, invalid_inputs, new_task

# Get Task ID in TASK_DB
def _get_new_taskID():
    return db.session.query(Task_DB).count() + 1

# Get Task ID
def get_new_taskID():
    return "TASK/" + str(_get_new_taskID())

# Get task_db data by using query
def get_Task_DB_by_query(
    statuses:list           = ALL_STATUS,
    start_due_date:datetime = None,
    end_due_date:datetime   = None,
    project:str             = '',
    name:str                = ''
):
    if (start_due_date is not None and end_due_date is not None):
        if (start_due_date > end_due_date):
            return None
    
    task_db_list = db.session.query(Task_DB)

    # Filter by Status
    if (len(statuses) > 0):
        task_db_list = task_db_list.filter(Task_DB.status.in_(statuses))
    
    # Filter by due_date
    if (start_due_date != None):
        task_db_list = task_db_list.filter(Task_DB.due_date >= start_due_date)
    if (end_due_date != None):
        task_db_list = task_db_list.filter(Task_DB.due_date <  end_due_date)
    
    if (project != ''):
        task_db_list = task_db_list.filter(Task_DB.project.contains(project))
    
    if (name != ''):
        task_db_list = task_db_list.filter(Task_DB.name.contains(name))

    return task_db_list

# Get analysis data from status point of view
def get_task_status_analysis_data(
    statuses:list,
    task_db_list:list
):
    # Get task status statistics for graph
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
                    task_db_list\
                        .filter(Task_DB.status == status)\
                        .count()
                )
                break

    return status_statistics

# Get analysis data from due date point of view
def get_task_dueDate_analysis_data(
    statuses:list,
    task_db_list
):

    dueDate_statistics = {
        'labels' : [],
        'data'   : {},
        'color'  : []
    }

    if (task_db_list.count() > 0):
        start_time_db = task_db_list.order_by(Task_DB.due_date).first()
        start_time    = Task(start_time_db).due_date.due_date
        end_time_db   = task_db_list.order_by(Task_DB.due_date.desc()).first()
        end_time      = Task(end_time_db).due_date.due_date
        date_list = []
        day = 0
        while(datetime.combine(start_time, time()) + timedelta(days=day) <= end_time):
            date_list.append(datetime.combine(start_time, time()) + timedelta(days=day))
            dueDate_statistics['labels'].append((start_time + timedelta(days=day)).strftime('%Y/%m/%d'))
            day += 1

        # Get task status statistics for graph
        for status in statuses:
            for status_info in STATUS_LIST.keys():
                if (status == STATUS_LIST[status_info]['str']):
                    dueDate_statistics['data'][status] = []
                    dueDate_statistics['color'].append(STATUS_LIST[status_info]['color'])
                    for start_date in date_list:
                        temp_start_time = datetime.combine(start_date, time())
                        temp_end_time = datetime.combine(temp_start_time + timedelta(days=1), time())
                        dueDate_statistics['data'][STATUS_LIST[status_info]['str']].append(
                            task_db_list\
                                .filter(Task_DB.status   == status)\
                                .filter(Task_DB.due_date >= temp_start_time)\
                                .filter(Task_DB.due_date <  temp_end_time)\
                                .count()
                        )
    
    return dueDate_statistics

# Get existed project list
def get_existed_option_list():
    existed_project_list = []
    task_db_list = db.session.query(Task_DB).all()
    for task_db in task_db_list:
        existed_project_list.append(str(task_db.project))
    existed_project_list = list(set(existed_project_list))
    return existed_project_list

# Check link condition
def check_link_condition(
    SourceTaskID:int,
    TargetTaskID:int,
    relationship:str
):
    link_flag = True

    # Check ID
    if (SourceTaskID == TargetTaskID):
        link_flag = False
    if (SourceTaskID < 1 or SourceTaskID > db.session.query(Task_DB).count()):
        link_flag = False
    if (TargetTaskID < 1 or TargetTaskID > db.session.query(Task_DB).count()):
        link_flag = False
    
    # Check Relationship
    if (relationship not in get_relationship_list()):
        link_flag = False
    
    # Check the relationship exist or not
    source_task = Task(SourceTaskID)
    for link in source_task.links:
        if (
            link["relationship"] == relationship
            and
            link["TaskID"] == TargetTaskID
        ):
            link_flag = False
    
    return link_flag

# Add Task Link
def add_task_link(
    SourceTaskID:int,
    TargetTaskID:int,
    relationship:str
):
    # Source Task
    source_task = Task(SourceTaskID)
    source_task.links.append({
        "relationship": relationship,
        "TaskID"      : TargetTaskID
    })
    source_task.update()

    # Target Task
    target_task = Task(TargetTaskID)
    pair_relationship = get_pair_relationship(relationship)
    target_task.links.append({
        "relationship": pair_relationship,
        "TaskID"      : SourceTaskID
    })
    target_task.update()

    return True

# Remove Task Link
def remove_task_link(
    SourceTaskID:int,
    TargetTaskID:int,
    relationship:str
):
    # Update Source Task
    SourceTask = Task(SourceTaskID)
    for idx,link in enumerate(SourceTask.links):
        if (
            link["TaskID"] == int(TargetTaskID)
            and
            link["relationship"] == relationship
        ):
            SourceTask.links.pop(idx)
            break
    SourceTask.update()

    # Update Target Task
    pair_relationship = get_pair_relationship(relationship)
    TargetTask = Task(TargetTaskID)
    for idx,link in enumerate(TargetTask.links):
        if (
            link["TaskID"] == int(SourceTaskID)
            and
            link["relationship"] == pair_relationship
        ):
            TargetTask.links.pop(idx)
            break
    TargetTask.update()

    return True
