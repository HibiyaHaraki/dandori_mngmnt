
"""
dandori_mngmnt.py
Main Flask application for Dandori Management system.
Defines all routes and main logic for task, comment, and link management.

Created by Hibiya Haraki, May 2025.
"""

from flask import render_template, request, url_for, redirect
from datetime import datetime, date, timedelta, time

# Application
from dandori_mngmnt import app

# Database Model
from dandori_mngmnt import db
from dandori_mngmnt.models.Task_DB     import Task_DB
from dandori_mngmnt.models.Comment_DB  import Comment_DB

# Required scripts
from dandori_mngmnt.script.Task     import *
from dandori_mngmnt.script.Comment  import *
from dandori_mngmnt.script.Due_date import *
from dandori_mngmnt.script.Status   import *
from dandori_mngmnt.script.Links    import *

# Static definition
NUMBER_OF_TODO = 10
NUMBER_OF_DAYS = 30

# Index page
@app.route('/', methods=['GET'])
def index():
    """
    Index page route. Shows the main task list and filter form.
    Returns:
        Rendered HTML for the index page.
    """
    # Inititalize input data
    form = {
        'status_info'    : STATUS_LIST,
        'status_selected': [],
        'start_due_date' : '',
        'end_due_date'   : '',
        'project'        : '',
        'name'           : ''
    }
    input_statuses = ALL_STATUS
    start_date     = datetime.combine(date.today(), time())
    end_date       = datetime.combine(date.today(), time()) + timedelta(days=NUMBER_OF_DAYS)
    project        = ''
    name           = ''

    # Get input
    temp_input_statuses = request.args.getlist("status")
    if (len(temp_input_statuses) > 0):
        input_statuses = temp_input_statuses
    for status_info in STATUS_LIST.values():
        if (status_info['str'] in input_statuses):
            form['status_selected'].append(True)
        else:
            form['status_selected'].append(False)
    
    temp_start_date_str = request.args.get('StartDueDate', '')
    if (temp_start_date_str != ''):
        start_date = datetime.strptime(temp_start_date_str,JS_TIME_FORMAT)
        form['start_due_date'] = temp_start_date_str
    else:
        form['start_due_date'] = start_date.strftime(JS_TIME_FORMAT)
    temp_end_date_str = request.args.get('EndDueDate', '')
    if (temp_end_date_str != ''):
        end_date   = datetime.strptime(temp_end_date_str,JS_TIME_FORMAT)
        form['end_due_date'] = temp_end_date_str
    else:
        form['end_due_date'] = end_date.strftime(JS_TIME_FORMAT)
    project = request.args.get('ProjectQuery', '')
    if (project != ''):
        form['project'] = project
    name    = request.args.get('NameQuery', '')
    if (name != ''):
        form['name'] = name

    # Get task data in table
    tasks_db_due_date = get_Task_DB_by_query(
        statuses = input_statuses,
        start_due_date = start_date,
        end_due_date = end_date,
        project = project,
        name = name
    ).order_by(Task_DB.due_date)

    tasks = []
    tasks_id = []
    for task_db in tasks_db_due_date.all():
        task = Task(task_db)
        tasks.append(task)
        tasks_id.append(task_db.id)
    
    project_option = get_existed_option_list()

    return render_template(
        'dandori_mngmnt/index.html',
        form=form,
        tasks = tasks,
        project_option = project_option
    )

# Kanban page
@app.route('/Kanban', methods=['GET'])
def kanban():
    """
    Kanban page route. Shows tasks in a Kanban-style board by status.
    Returns:
        Rendered HTML for the Kanban page.
    """
    if (request.method == 'GET'):
        # Inititalize input data
        form = {
            'status_info'    : STATUS_LIST,
            'status_selected': [],
            'start_due_date' : '',
            'end_due_date'   : '',
            'project'        : '',
            'name'           : ''
        }
        input_statuses = ALL_STATUS
        start_date     = datetime.combine(date.today(), time())
        end_date       = datetime.combine(date.today(), time()) + timedelta(days=NUMBER_OF_DAYS)
        project        = ''
        name           = ''

        # Get input
        temp_input_statuses = request.args.getlist("status")
        if (len(temp_input_statuses) > 0):
            input_statuses = temp_input_statuses
        for status_info in STATUS_LIST.values():
            if (status_info['str'] in input_statuses):
                form['status_selected'].append(True)
            else:
                form['status_selected'].append(False)
        
        temp_start_date_str = request.args.get('StartDueDate', '')
        if (temp_start_date_str != ''):
            start_date = datetime.strptime(temp_start_date_str,JS_TIME_FORMAT)
            form['start_due_date'] = temp_start_date_str
        else:
            form['start_due_date'] = start_date.strftime(JS_TIME_FORMAT)
        temp_end_date_str = request.args.get('EndDueDate', '')
        if (temp_end_date_str != ''):
            end_date   = datetime.strptime(temp_end_date_str,JS_TIME_FORMAT)
            form['end_due_date'] = temp_end_date_str
        else:
            form['end_due_date'] = end_date.strftime(JS_TIME_FORMAT)
        project = request.args.get('ProjectQuery', '')
        if (project != ''):
            form['project'] = project
        name    = request.args.get('NameQuery', '')
        if (name != ''):
            form['name'] = name
        
        # Get task data in table
        tasks_db_due_date = get_Task_DB_by_query(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date,
            project = project,
            name = name
        ).order_by(Task_DB.due_date)
        tasks = []
        tasks_id = []
        for task_db in tasks_db_due_date.all():
            task = Task(task_db)
            tasks.append(task)
            tasks_id.append(task_db.id)
        
        project_option = get_existed_option_list()

        # Get specific tasks
        return render_template(
            'dandori_mngmnt/kanban.html',
            form=form,
            tasks = tasks,
            project_option = project_option
        )

# Task Link Overview page
@app.route('/TASK_LINK', methods=['GET'])
def task_link():
    """
    Task link overview page route. Shows all task relationships and Mermaid chart.
    Returns:
        Rendered HTML for the task link overview page.
    """
    if (request.method == 'GET'):
        # Inititalize input data
        form = {
            'status_info'    : STATUS_LIST,
            'status_selected': [],
            'start_due_date' : '',
            'end_due_date'   : '',
            'project'        : '',
            'name'           : ''
        }
        input_statuses = ALL_STATUS
        start_date     = datetime.combine(date.today(), time())
        end_date       = datetime.combine(date.today(), time()) + timedelta(days=NUMBER_OF_DAYS)
        project        = ''
        name           = ''

        # Get input
        temp_input_statuses = request.args.getlist("status")
        if (len(temp_input_statuses) > 0):
            input_statuses = temp_input_statuses
        for status_info in STATUS_LIST.values():
            if (status_info['str'] in input_statuses):
                form['status_selected'].append(True)
            else:
                form['status_selected'].append(False)
        
        temp_start_date_str = request.args.get('StartDueDate', '')
        if (temp_start_date_str != ''):
            start_date = datetime.strptime(temp_start_date_str,JS_TIME_FORMAT)
            form['start_due_date'] = temp_start_date_str
        else:
            form['start_due_date'] = start_date.strftime(JS_TIME_FORMAT)
        temp_end_date_str = request.args.get('EndDueDate', '')
        if (temp_end_date_str != ''):
            end_date   = datetime.strptime(temp_end_date_str,JS_TIME_FORMAT)
            form['end_due_date'] = temp_end_date_str
        else:
            form['end_due_date'] = end_date.strftime(JS_TIME_FORMAT)
        project = request.args.get('ProjectQuery', '')
        if (project != ''):
            form['project'] = project
        name    = request.args.get('NameQuery', '')
        if (name != ''):
            form['name'] = name
        
        # Get task data in table
        tasks_db_due_date = get_Task_DB_by_query(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date,
            project = project,
            name = name
        ).order_by(Task_DB.due_date)
        tasks = []
        tasks_id = []
        for task_db in tasks_db_due_date.all():
            task = Task(task_db)
            tasks.append(task)
            tasks_id.append(task_db.id)
        
        tasks_db = db.session.query(Task_DB).filter(Task_DB.id.in_(tasks_id))

        # Get Task link chart
        mermaid_command_input = []
        link_info = []
        for task_db in tasks_db:
            temp_mermaid_command_input = Task(task_db)._mermaid_command_input()
            for command in temp_mermaid_command_input:
                mermaid_command_input.append(command)
        for command in remove_duplicated_relationship(mermaid_command_input):    
            temp_link_info = {
                "TargetTask"   : Task(int(command["TargetTaskID"])),
                "SourceTask"   : Task(int(command["SourceTaskID"])),
                "relationship" : command["relationship"] 
            }
            link_info.append(temp_link_info)
        
        link_chart = generate_mermaid_command(mermaid_command_input)
        
        project_option = get_existed_option_list()

        # Get specific tasks
        return render_template(
            'dandori_mngmnt/task_link.html',
            form=form,
            tasks = tasks,
            project_option = project_option,
            chart_links = link_chart,
            links = link_info
        )

# Task Overview page
@app.route('/TASK', methods=['GET'])
def task():
    """
    Task overview page route. Shows statistics, analysis, and all tasks.
    Returns:
        Rendered HTML for the task overview page.
    """
    if (request.method == 'GET'):
        # Inititalize input data
        form = {
            'status_info'    : STATUS_LIST,
            'status_selected': [],
            'start_due_date' : '',
            'end_due_date'   : '',
            'project'        : '',
            'name'           : ''
        }
        input_statuses = ALL_STATUS
        start_date     = datetime.combine(date.today(), time())
        end_date       = datetime.combine(date.today(), time()) + timedelta(days=NUMBER_OF_DAYS)
        project        = ''
        name           = ''

        # Get input
        temp_input_statuses = request.args.getlist("status")
        if (len(temp_input_statuses) > 0):
            input_statuses = temp_input_statuses
        for status_info in STATUS_LIST.values():
            if (status_info['str'] in input_statuses):
                form['status_selected'].append(True)
            else:
                form['status_selected'].append(False)
        
        temp_start_date_str = request.args.get('StartDueDate', '')
        if (temp_start_date_str != ''):
            start_date = datetime.strptime(temp_start_date_str,JS_TIME_FORMAT)
            form['start_due_date'] = temp_start_date_str
        else:
            form['start_due_date'] = start_date.strftime(JS_TIME_FORMAT)
        temp_end_date_str = request.args.get('EndDueDate', '')
        if (temp_end_date_str != ''):
            end_date   = datetime.strptime(temp_end_date_str,JS_TIME_FORMAT)
            form['end_due_date'] = temp_end_date_str
        else:
            form['end_due_date'] = end_date.strftime(JS_TIME_FORMAT)
        project = request.args.get('ProjectQuery', '')
        if (project != ''):
            form['project'] = project
        name    = request.args.get('NameQuery', '')
        if (name != ''):
            form['name'] = name
        
        # Get task data in table
        tasks_db_due_date = get_Task_DB_by_query(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date,
            project = project,
            name = name
        ).order_by(Task_DB.due_date)
        tasks = []
        tasks_id = []
        for task_db in tasks_db_due_date.all():
            task = Task(task_db)
            tasks.append(task)
            tasks_id.append(task_db.id)
        
        # Get next due date
        tasks_db_next_due_date = get_Task_DB_by_query(
            statuses = input_statuses,
            project = project,
            name = name
        ).order_by(Task_DB.due_date)
        
        tasks_db = db.session.query(Task_DB).filter(Task_DB.id.in_(tasks_id))

        # Get task status statistics for graph
        status_statistics = get_task_status_analysis_data(
            statuses = input_statuses,
            task_db_list = tasks_db
        )

        # Get step due_date statistics for graph
        due_date_statistics = get_task_dueDate_analysis_data(
            statuses = input_statuses,
            task_db_list = tasks_db
        )

        # Get Task link chart
        mermaid_command_input = []
        for task_db in tasks_db:
            temp_mermaid_command_input = Task(task_db)._mermaid_command_input()
            for command in temp_mermaid_command_input:
                mermaid_command_input.append(command)
        
        link_chart = generate_mermaid_command(mermaid_command_input)
        
        project_option = get_existed_option_list()

        # Get specific tasks
        return render_template(
            'dandori_mngmnt/task.html',
            form=form,
            status_statistics = status_statistics,
            due_date_statistics = due_date_statistics,
            tasks = tasks,
            project_option = project_option,
            chart_links = link_chart
        )

# Task detail Page
@app.route('/TASK/<int:id>', methods=['GET', 'POST'])
def task_detail(id):
    """
    Task detail page route. Shows details, comments, and links for a task.
    Args:
        id (int): Task ID.
    Returns:
        Rendered HTML for the task detail page.
    """
    if (request.method == 'GET'):
        task_data = Task(id)
        project_option = get_existed_option_list()

        # Link Task
        link_tasks  = []
        chart_links = task_data.get_mermaid_command()
        for link in task_data.links:
            link_tasks.append({
                "relationship": link["relationship"],
                "Task"        : Task(link["TaskID"])
            })
        

        return render_template(
            'dandori_mngmnt/task_detail.html',
            task  = task_data,
            comments = task_data.get_comments(),
            parent_id = id,
            project_option = project_option,
            link_tasks = link_tasks,
            chart_links = chart_links
        )


# Task add comment
@app.route('/TASK/<int:id>/add_comment', methods=['POST'])
def task_add_comment(id):
    """
    Add a comment to a task.
    Args:
        id (int): Task ID.
    Returns:
        Redirect to the task detail page.
    """
    if (request.method == 'POST'):
        form_comment = request.form.get('AddComment')
        if (len(form_comment) > 0):
            new_commentID = add_new_comment(form_comment)
            task_data = Task(id)
            task_data.comments.append(new_commentID)
            task_data.update()
            return redirect(url_for('task_detail', id=id))
        else:
            pass

# Task edit comment
@app.route('/TASK/<int:task_id>/edit_comment/<int:comment_id>', methods=['POST'])
def task_edit_comment(task_id, comment_id):
    """
    Edit a comment for a task.
    Args:
        task_id (int): Task ID.
        comment_id (int): Comment ID.
    Returns:
        Redirect to the task detail page.
    """
    if (request.method == 'POST'):
        form_comment    = request.form.get('EditComment')
        current_comment = Comment(int(comment_id))
        if (current_comment.comment != form_comment):
            current_comment.update(form_comment)
            return redirect(url_for('task_detail', id=task_id))

# Task delete comment
@app.route('/TASK/<int:task_id>/delete_comment/<int:comment_id>', methods=['GET'])
def task_delete_comment(task_id, comment_id):
    """
    Delete a comment from a task.
    Args:
        task_id (int): Task ID.
        comment_id (int): Comment ID.
    Returns:
        Redirect to the task detail page.
    """
    if (request.method == 'GET'):
        current_task = Task(task_id)
        current_task.comments.remove(int(comment_id))
        current_task.update()
        return redirect(url_for('task_detail', id=task_id))

# Edit Task data
@app.route('/TASK/<int:id>/edit_task', methods=['POST'])
def edit_task(id):
    """
    Edit a task's details.
    Args:
        id (int): Task ID.
    Returns:
        Redirect to the task detail page.
    """
    if (request.method == 'POST'):
        task = Task(id)

        # Get form data
        form_name         = request.form.get('TaskName')
        form_project      = request.form.get('TaskProject')
        form_assignedby   = request.form.get('TaskAssignedBy')
        form_str_due_date = request.form.get('TaskDueDate')
        form_criteria     = request.form.get('TaskCriteria')
        form_description  = request.form.get('TaskDescription')
        form_step_order   = request.form.get('TaskStepOrder')

        invalid_input_flag, invalid_inputs = check_task_input(
            form_name,
            form_str_due_date,
            form_criteria,
            form_assignedby,
            form_project,
            form_description
        )

        if (not invalid_input_flag):
            task.name        = form_name
            task.due_date    = Due_date(datetime.strptime(form_str_due_date, JS_TIME_FORMAT))
            task.criteria    = form_criteria
            task.assigned_by = form_assignedby
            task.project     = form_project
            task.description = form_description

            task.update()
        
        return redirect(url_for('task_detail', id=id))

# Page for adding the new task with link
@app.route('/TASK/<int:task_id>/create_linked_task', methods=['GET', 'POST'])
def create_linked_task(task_id):
    """
    Create a new task and link it to an existing task.
    Args:
        task_id (int): The ID of the task to link to.
    Returns:
        Rendered HTML for the create linked task page or redirect.
    """
    if (request.method == 'GET'):
        new_taskID = get_new_taskID()
        project_option = get_existed_option_list()
        return render_template(
            'dandori_mngmnt/create_linked_task.html',
            new_taskID = new_taskID,
            invalid_input_flag = False,
            invalid_inputs = [],
            project_option = project_option,
            task = Task(task_id),
            relationships = get_relationship_list()
        )
    
    if (request.method == 'POST'):
        # Get form data
        form_name         = request.form.get('TaskName')
        form_project      = request.form.get('TaskProject')
        form_assignedby   = request.form.get('TaskAssignedBy')
        form_str_due_date = request.form.get('TaskDueDate')
        form_criteria     = request.form.get('TaskCriteria')
        form_description  = request.form.get('TaskDescription')

        invalid_input_flag, invalid_inputs, new_task = add_new_Task(
            form_name, form_str_due_date, form_criteria, form_assignedby,
            form_project     = form_project,
            form_description = form_description
        )

        # Error input
        if (invalid_input_flag):
            new_taskID = get_new_taskID()
            project_option = get_existed_option_list()
            return render_template(
                'dandori_mngmnt/create_task.html',
                new_taskID = new_taskID,
                invalid_input_flag = invalid_input_flag,
                invalid_inputs = invalid_inputs,
                project_option = project_option
            )
        
        db.session.add(new_task)
        db.session.commit()
        db.session.refresh(new_task)

        if (invalid_input_flag):
            new_taskID = get_new_taskID()
            project_option = get_existed_option_list()
            return render_template(
                'dandori_mngmnt/create_task.html',
                new_taskID = new_taskID,
                invalid_input_flag = invalid_input_flag,
                invalid_inputs = invalid_inputs,
                project_option = project_option
            )

        created_Task = Task(new_task.id)
        created_Task.update()

        # Get inputs
        SourceTaskID = new_task.id
        TargetTaskID = task_id
        relationship = request.form.get('Relationship_Check')

        # Check condition
        link_flag = check_link_condition(
            SourceTaskID,
            TargetTaskID,
            relationship
        )

        if (link_flag):
            res = add_task_link(
                SourceTaskID,
                TargetTaskID,
                relationship
            )
        
        return redirect(url_for('task_detail', id=new_task.id))

# Page for adding the new task
@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    """
    Create a new task.
    Returns:
        Rendered HTML for the create task page or redirect.
    """
    if (request.method == 'GET'):
        new_taskID = get_new_taskID()
        project_option = get_existed_option_list()
        return render_template(
            'dandori_mngmnt/create_task.html',
            new_taskID = new_taskID,
            invalid_input_flag = False,
            invalid_inputs = [],
            project_option = project_option
        )
    
    if (request.method == 'POST'):
        # Get form data
        form_name         = request.form.get('TaskName')
        form_project      = request.form.get('TaskProject')
        form_assignedby   = request.form.get('TaskAssignedBy')
        form_str_due_date = request.form.get('TaskDueDate')
        form_criteria     = request.form.get('TaskCriteria')
        form_description  = request.form.get('TaskDescription')

        invalid_input_flag, invalid_inputs, new_task = add_new_Task(
            form_name, form_str_due_date, form_criteria, form_assignedby,
            form_project     = form_project,
            form_description = form_description
        )

        # Error input
        if (invalid_input_flag):
            new_taskID = get_new_taskID()
            project_option = get_existed_option_list()
            return render_template(
                'dandori_mngmnt/create_task.html',
                new_taskID = new_taskID,
                invalid_input_flag = invalid_input_flag,
                invalid_inputs = invalid_inputs,
                project_option = project_option
            )
        
        db.session.add(new_task)
        db.session.commit()
        db.session.refresh(new_task)
        parent_taskID = new_task.id

        if (invalid_input_flag):
            new_taskID = get_new_taskID()
            project_option = get_existed_option_list()
            return render_template(
                'dandori_mngmnt/create_task.html',
                new_taskID = new_taskID,
                invalid_input_flag = invalid_input_flag,
                invalid_inputs = invalid_inputs,
                project_option = project_option
            )

        created_Task = Task(parent_taskID)
        created_Task.update()
        
        return redirect(url_for('task_detail', id=parent_taskID))

# Change status of task
@app.route('/TASK/<int:id>/change_state', methods=['GET'])
def step_change_state(id):
    """
    Change the status of a task to the next state.
    Args:
        id (int): Task ID.
    Returns:
        Redirect to the task detail page.
    """
    if (request.method == 'GET'):

        # Update Step status
        task = Task(id)
        next_state_str = str(request.args.get('next_state', ''))
        task.status.change_state(next_state_str)
        task.update()

        return redirect(url_for('task_detail', id=id))

# Add link to Task
@app.route('/TASK/<int:id>/add_link', methods=['GET','POST'])
def task_add_link(id):
    """
    Add a link between two tasks.
    Args:
        id (int): Source Task ID.
    Returns:
        Rendered HTML for the add link page or redirect.
    """
    if (request.method == 'GET'):
        # Get Task ID
        task = Task(id)

        # Init
        target_task_id = 1
        target_task = Task(1)
        target_task_relatinship = ""

        # Get input
        target_task_id = request.args.get('TargetTaskID_Check','')
        target_task_relatinship = request.args.get('Relationship_Check','')

        # Get target Task ID
        if (target_task_id != ''):
            target_task_id = int(target_task_id)
            if (
                target_task_id > 0
                and
                target_task_id <= db.session.query(Task_DB).count()
            ):
                target_task = Task(target_task_id)

        return render_template(
            'dandori_mngmnt/task_add_link.html',
            task  = task,
            relationships = get_relationship_list(),
            target_task = target_task,
            target_task_relationship = target_task_relatinship
        )
    
    if (request.method == 'POST'):
        # Get inputs
        SourceTaskID = int(request.form.get('SourceTaskID_Confirm'))
        TargetTaskID = int(request.form.get('TargetTaskID_Confirm'))
        relationship =     request.form.get('Relationship_Confirm')

        # Check condition
        link_flag = check_link_condition(
            SourceTaskID,
            TargetTaskID,
            relationship
        )

        if (link_flag):
            res = add_task_link(
                SourceTaskID,
                TargetTaskID,
                relationship
            )
        
        return redirect(url_for('task_detail', id=SourceTaskID))

# Add link to Task
@app.route('/TASK/<int:id>/remove_link', methods=['GET'])
def task_remove_link(id):
    """
    Remove a link between two tasks.
    Args:
        id (int): Source Task ID.
    Returns:
        Redirect to the task detail page.
    """
    # Get input
    SourceTaskID = id
    TargetTaskID = int(request.args.get('TaskID',''))
    relationship = request.args.get('Relationship','')

    remove_task_link(
        SourceTaskID,
        TargetTaskID,
        relationship
    )

    return redirect(url_for('task_detail', id=id))

