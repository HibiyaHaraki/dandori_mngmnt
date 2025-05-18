# Dandori Management

May 2025, created by Hibiya Haraki

The risk of running this script is always with you.

## What is Dandori Management?
A lot of new-grads learn that Dnadori is most important to work as adult. However, I am not good at doing this. Therefore, I created a Todo manageement application which focus on the work steps. This app runon browther and created by Python Flask.

## Build environment

### Install Python 
You ned to install [Python](https://www.python.org/downloads/release/python-3110/) at first. 

### Install necessary modules
Then you need to install Flask by following commands.

```
pip install flask flask-sqlalchemy
pip install sounddevice  pyttsx3 
pip install vosk
pip install transformers torch scipy
```

# Download vosk model
1. Please access to [Vosk Models](https://alphacephei.com/vosk/models) and download ["vosk-model-en-us-0.22-lgraph"](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip)
2. Please unzip and put under your repo as "model-en-sm"

### Start dandori_mngmnt Web app
After that, you can start this web application by following command.

```
start_dandori_mngmnt.bat
```

### Start dandori_mngmnt Sound app
After that, you can start sound application by following command.

```
start_dandori_sound.bat
```

## How to use this Web app
This Todo management app have 2 kind of to do format

### Data type
In this application we manage our to do by splitting 2 types of data.

1. Task
2. Step

In this app, we think that we get "Task" from other person. Then we make "Steps" for achieve the "Task".

### How to create Task
1. You can create Task by the button at top page.
    ![Top page](img/Top_Page.png)
2. You need to input the necessary information about "Task"
    ![Task Create Page](img/Create_Task_Window.png)

### How to create Step
"Step" is the process for achieving a "Task". Therefore, we can create "Step" only under specific "Task". 

1. We need to select a task you want to add "Step". Then start to create "Step".
    ![Task Page](img/Task_Page.png)
2. Then, we need to input some information for creating "Step".
    ![Step Create Page](img/Create_Step_Window.png)
3. On the task page you can see added step for achieving a "Task"
    ![Result of adding new Step](img/Step_added_result.png)

### Functions
On this function, we can do following things.
* Create new Task & Steps
* Edit existed Task & Steps
* Check the statistic result of Task & Step by graph
    ![Step statistic page](img/Step_statistic_page.png)
* Add comment on each Task & Step
* Manage the statusof each Task & Steps (We can change the Step status manually. Task status automatically change due to the steps status.)
    ![Status Management](img/Status_Managementr.png)

## What is possible reaction for sound app?
Currently this app can respond only following question.
* What kind of task do I have to do today?