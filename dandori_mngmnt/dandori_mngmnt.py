#
# May 2025. Created by Hibiya Haraki
#
# dandori_mngmnt.py
#

from flask import render_template, request, url_for, redirect
from datetime import datetime, date, timedelta, time
import json, copy

# Application
from dandori_mngmnt import app

# Database Model
from dandori_mngmnt import db
from dandori_mngmnt.models.Task_DB     import Task_DB
from dandori_mngmnt.models.Step_DB     import Step_DB
from dandori_mngmnt.models.Comment_DB  import Comment_DB

# Required scripts
from dandori_mngmnt.script.Task     import *
from dandori_mngmnt.script.Step     import *
from dandori_mngmnt.script.Comment  import *
from dandori_mngmnt.script.Due_date import *
from dandori_mngmnt.script.Status   import *

# Static definition
NUMBER_OF_TODO = 20
NUMBER_OF_DAYS = 30

# Index.html
@app.route('/')
def index():
    # Get tasks
    filtered_tasks_db = db.session.query(Task_DB) \
        .filter(Task_DB.status != "DONE") \
        .order_by(Task_DB.due_date) \
        .order_by(Task_DB.id.desc()) \
        .limit(NUMBER_OF_TODO)
    to_do_tasks = []
    for task_db in filtered_tasks_db:
        task = Task(task_db)
        to_do_tasks.append(task)

    # Get Steps
    filtered_steps_db = db.session.query(Step_DB) \
        .filter(Step_DB.status != "DONE") \
        .order_by(Step_DB.due_date) \
        .order_by(Step_DB.id.desc()) \
        .limit(NUMBER_OF_TODO)
    to_do_steps = []
    for step_db in filtered_steps_db:
        step = Step(step_db)
        to_do_steps.append(step)
    return render_template(
        'dandori_mngmnt/index.html',
        to_do_tasks = to_do_tasks,
        to_do_steps = to_do_steps
    )

# Task.html
@app.route('/TASK', methods=['GET'])
def task():
    if (request.method == 'GET'):
        # Inititalize input data
        form = {
            'status_info'    : STATUS_LIST,
            'status_selected': [],
            'start_due_date' : '',
            'end_due_date'   : ''
        }
        input_statuses = ALL_STATUS
        start_date      = datetime.today()
        end_date        = datetime.today() + timedelta(days=NUMBER_OF_DAYS)

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

        # Get task status statistics for graph
        status_statistics = get_task_status_analysis_data(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date
        )

        # Get step due_date statistics for graph
        due_date_statistics = get_task_dueDate_analysis_data(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date
        )
        
        # Get task data in table
        tasks_db = get_Task_DB_by_query(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date
        ).order_by(Task_DB.due_date).all()
        tasks = []
        for task_db in tasks_db:
            task = Task(task_db)
            tasks.append(task) 

        # Get specific tasks
        return render_template(
            'dandori_mngmnt/task.html',
            form=form,
            status_statistics = status_statistics,
            due_date_statistics = due_date_statistics,
            tasks = tasks
        )


@app.route('/STEP', methods=['GET'])
def step():
    if (request.method == 'GET'):
        # Inititalize input data
        form = {
            'status_info'    : STATUS_LIST,
            'status_selected': [],
            'start_due_date' : '',
            'end_due_date'   : ''
        }
        input_statuses = ALL_STATUS
        start_date      = datetime.today()
        end_date        = datetime.today() + timedelta(days=NUMBER_OF_DAYS)

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

        # Get task status statistics for graph
        status_statistics = get_step_status_analysis_data(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date
        )

        # Get step due_date statistics for graph
        due_date_statistics = get_step_dueDate_analysis_data(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date
        )

        # Get step data in table
        steps_db = get_Step_DB_by_query(
            statuses = input_statuses,
            start_due_date = start_date,
            end_due_date = end_date
        ).order_by(Step_DB.due_date).all()
        steps = []
        for step_db in steps_db:
            step = Step(step_db)
            steps.append(step) 

        # Get specific tasks
        return render_template(
            'dandori_mngmnt/step.html',
            form=form,
            status_statistics = status_statistics,
            due_date_statistics = due_date_statistics,
            steps = steps
        )

# Task detail Page
@app.route('/TASK/<int:id>', methods=['GET', 'POST'])
def task_detail(id):
    if (request.method == 'GET'):
        task_data = Task(id)
        steps     = task_data.get_steps()
        return render_template(
            'dandori_mngmnt/task_detail.html',
            task  = task_data,
            steps = steps,
            comments = task_data.get_comments(),
            parent_id = id
        )


# Task add comment
@app.route('/TASK/<int:id>/add_comment', methods=['POST'])
def task_add_comment(id):
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
    if (request.method == 'POST'):
        form_comment    = request.form.get('EditComment')
        current_comment = Comment(int(comment_id))
        if (current_comment.comment != form_comment):
            current_comment.update(form_comment)
            return redirect(url_for('task_detail', id=task_id))

# Task delete comment
@app.route('/TASK/<int:task_id>/delete_comment/<int:comment_id>', methods=['GET'])
def task_delete_comment(task_id,comment_id):
    if (request.method == 'GET'):
        current_task = Task(task_id)
        current_task.comments.remove(int(comment_id))
        current_task.update()
        return redirect(url_for('task_detail', id=task_id))

'''
@app.route('/TASK/<int:id>/change_state', methods=['GET'])
def task_change_state(id):
    if (request.method == 'GET'):
        task = Task(id)
        next_state_str = str(request.args.get('next_state', ''))
        task.status.change_state(next_state_str)
        task.update()
        return redirect(url_for('task_detail', id=id))
'''

@app.route('/TASK/<int:id>/edit_task', methods=['POST'])
def edit_task(id):
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
            task.steps       = json.loads(form_step_order)

            task.update()
        
        return redirect(url_for('task_detail', id=id))

# Step detail Page
@app.route('/STEP/<int:id>')
def step_detail(id):
    step_data    = Step(id)
    parent_task = Task(step_data.parent_task)
    return render_template(
        'dandori_mngmnt/step_detail.html',
        step = step_data,
        parent_task = parent_task,
        comments = step_data.get_comments(),
        steps = parent_task.get_steps(),
        parent_id = id
    )

# Step add comment
@app.route('/STEP/<int:id>/add_comment', methods=['POST'])
def step_add_comment(id):
    if (request.method == 'POST'):
        form_comment = request.form.get('AddComment')
        if (len(form_comment) > 0):
            new_commentID = add_new_comment(form_comment)
            step_data = Step(id)
            step_data.comments.append(new_commentID)
            step_data.update()
            return redirect(url_for('step_detail', id=id))
        else:
            pass

# Step edit comment
@app.route('/STEP/<int:step_id>/edit_comment/<int:comment_id>', methods=['POST'])
def step_edit_comment(step_id, comment_id):
    if (request.method == 'POST'):
        form_comment    = request.form.get('EditComment')
        current_comment = Comment(int(comment_id))
        if (current_comment.comment != form_comment):
            current_comment.update(form_comment)
            return redirect(url_for('step_detail', id=step_id))

# Step delete comment
@app.route('/STEP/<int:step_id>/delete_comment/<int:comment_id>', methods=['GET'])
def step_delete_comment(step_id,comment_id):
    if (request.method == 'GET'):
        current_step = Step(step_id)
        current_step.comments.remove(int(comment_id))
        current_step.update()
        return redirect(url_for('step_detail', id=step_id))

@app.route('/STEP/<int:id>/change_state', methods=['GET'])
def step_change_state(id):
    if (request.method == 'GET'):
        # Update Step status
        step = Step(id)
        next_state_str = str(request.args.get('next_state', ''))
        step.status.change_state(next_state_str)
        step.update()

        # Update Task status
        parent_task = Task(step.parent_task)
        parent_task.update_TaskStatus()
        parent_task.update()
        return redirect(url_for('step_detail', id=id))

@app.route('/STEP/<int:id>/edit_step', methods=['POST'])
def edit_step(id):
    if (request.method == 'POST'):
        step = Step(id)

        # Get form data
        form_name         = request.form.get('StepName')
        form_str_due_date = request.form.get('StepDueDate')
        form_criteria     = request.form.get('StepCriteria')
        form_description  = request.form.get('StepDescription')

        invalid_input_flag, invalid_inputs = check_step_input(
            form_name,
            form_str_due_date,
            form_criteria,
            step.parent_task,
            form_description
        )

        if (not invalid_input_flag):
            step.name        = form_name
            step.due_date    = Due_date(datetime.strptime(form_str_due_date, JS_TIME_FORMAT))
            step.criteria    = form_criteria
            step.description = form_description

            step.update()
        
        return redirect(url_for('step_detail', id=id))


# Page for adding the new task
@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if (request.method == 'GET'):
        new_taskID = get_new_taskID()
        return render_template(
            'dandori_mngmnt/create_task.html',
            new_taskID = new_taskID,
            invalid_input_flag = False,
            invalid_inputs = []
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
            return render_template(
                'dandori_mngmnt/create_task.html',
                new_taskID = new_taskID,
                invalid_input_flag = invalid_input_flag,
                invalid_inputs = invalid_inputs
            )
        
        db.session.add(new_task)
        db.session.commit()
        db.session.refresh(new_task)
        parent_taskID = new_task.id

        invalid_input_flag, invalid_inputs, new_step = add_new_Step(
            "Create steps for \"{0}\"".format(form_name), 
            form_str_due_date, 
            "Finish creating Steps for \"{0}\"".format(form_name), 
            parent_taskID
        )

        if (invalid_input_flag):
            new_taskID = get_new_taskID()
            return render_template(
                'dandori_mngmnt/create_task.html',
                new_taskID = new_taskID,
                invalid_input_flag = invalid_input_flag,
                invalid_inputs = invalid_inputs
            )

        db.session.add(new_step)
        db.session.commit()
        db.session.refresh(new_step)
        stepID = new_step.id

        created_Task = Task(parent_taskID)
        created_Task.steps.append(stepID)
        created_Task.update()
        
        return redirect(url_for('task_detail', id=parent_taskID))
            
# Page for adding new step
@app.route('/TASK/<int:parent_taskID>/create_step', methods=['GET', 'POST'])
def create_step(parent_taskID):
    if (request.method == 'GET'):
        new_stepID = get_new_stepID()
        parent_task = Task(parent_taskID)
        return render_template(
            'dandori_mngmnt/create_step.html',
            new_stepID = new_stepID,
            parent_task = parent_task,
            invalid_input_flag = False,
            invalid_inputs = []
        )
    
    if (request.method == 'POST'):
        # Get form data
        form_name         = request.form.get('StepName')
        form_str_due_date = request.form.get('StepDueDate')
        form_criteria     = request.form.get('StepCriteria')
        form_description  = request.form.get('StepDescription')

        invalid_input_flag, invalid_inputs, new_step = add_new_Step(
            form_name, form_str_due_date, form_criteria, parent_taskID,
            form_description=form_description
        )

        # Input Error
        if (invalid_input_flag):
            new_stepID = get_new_stepID()
            parent_task = Task(parent_taskID)
            return render_template(
                'dandori_mngmnt/create_step.html',
                new_stepID = new_stepID,
                parent_task = parent_task,
                invalid_input_flag = invalid_input_flag,
                invalid_inputs = invalid_inputs
            )
        
        # Create new Step objec data
        db.session.add(new_step)
        db.session.commit()
        db.session.refresh(new_step)
        new_stepID = new_step.id
        parent_task = Task(parent_taskID)
        parent_task.steps.append(new_stepID)
        parent_task.update_TaskStatus()
        parent_task.update()

        return redirect(url_for('task_detail', id=parent_taskID))

