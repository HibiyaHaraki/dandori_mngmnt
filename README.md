

# 🚀 Dandori Management


**🖥️ GUI App for cupposting task management by using ticket.**  
⚠️ The risk of running this script is always with you.


---


## ✨ Features

- 🗂️ Web-based task management with Kanban and list views
- 📝 Task creation, editing, linking, and status transitions
- 💬 Commenting system for tasks
- 📅 Project and due date filtering
- 🕸️ Visual task relationship diagrams (Mermaid.js)
- 📊 Task statistics and analysis (Chart.js)
- 🗄️ Simple SQLite backend (via SQLAlchemy)
- 🎨 Bootstrap-based UI

---


## 🏗️ Project Structure

```
dandori_app_dev/
│
├── server.py                # Entry point for running the Flask app
├── start_dandori_mngmnt.bat # Batch file to start the server and open browser
├── Pipfile / Pipfile.lock   # Python dependencies
│
├── dandori_mngmnt/
│   ├── __init__.py          # Flask app and DB initialization
│   ├── config.py            # App configuration
│   ├── dandori_mngmnt.py    # Main Flask routes and logic
│   ├── models/
│   │   ├── Task_DB.py       # SQLAlchemy model for tasks
│   │   └── Comment_DB.py    # SQLAlchemy model for comments
│   ├── script/
│   │   ├── Task.py          # Task logic and DB operations
│   │   ├── Comment.py       # Comment logic
│   │   ├── Due_date.py      # Due date handling
│   │   ├── Status.py        # Status definitions and transitions
│   │   └── Links.py         # Task linking and Mermaid diagram logic
│   ├── static/
│   │   └── css/             # Custom CSS
│   └── templates/           # Jinja2 HTML templates
│
├── instance/
│   └── dandori_mngmnt.db    # SQLite database (auto-created)
└── plan/
    └── dandori_management_class.drawio # System design diagram
```

---


## ⚙️ Requirements

- Python 3.11
- Flask
- Flask-SQLAlchemy
- SQLAlchemy


💡 To install the main dependencies, run:
```
pip install flask flask-sqlalchemy sqlalchemy
```

---


## 🚦 Getting Started


▶️ Start the server with:
```
python server.py 5000
```
🪟 Or use the batch file (Windows):
```
start_dandori_mngmnt.bat
```
🌐 Then open [http://localhost:5000](http://localhost:5000) in your browser.

---


## 🛠️ Usage

- **🗂️ Task List:** View, filter, and search tasks.
- **📋 Kanban Board:** Visualize tasks by status.
- **🔍 Task Detail:** View and edit task details, comments, and links.
- **✏️ Create/Edit Task:** Add new tasks or update existing ones.
- **🔗 Link Tasks:** Define relationships between tasks (e.g., blocks, contains).
- **📈 Analysis:** View task statistics and due date analysis.

---


## 🧰 Technologies Used


[![HTML5](https://img.shields.io/badge/HTML5-grey.svg?logo=html5&style=flat)](https://www.w3.org/html/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-grey.svg?logo=bootstrap&style=flat)](https://getbootstrap.jp/)
[![PYTHON](https://img.shields.io/badge/python-grey.svg?logo=python&style=flat)](https://www.python.org/downloads/release/python-3110/)
[![FLASK](https://img.shields.io/badge/FLASK-grey.svg?logo=flask&style=flat)](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-grey.svg?logo=sqlalchemy&style=flat)](https://www.sqlalchemy.org/)
[![Mermaid](https://img.shields.io/badge/Mermaid-grey.svg?logo=mermaid&style=flat)](https://mermaid.js.org/)
[![Char.js](https://img.shields.io/badge/Chart.js-grey.svg?logo=chart.js&style=flat)](https://www.chartjs.org/)