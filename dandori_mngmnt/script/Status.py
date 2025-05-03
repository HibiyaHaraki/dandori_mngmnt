#
# May 2025. Created by Hibiya Haraki
#
# status_control.py
#

STATUS_LIST = {
        "open_state" : {
            "str"        : "OPEN",
            "color"      : "secondary",
            "transition" :[
                "progress_state",
                "wait_state",
                "done_state"
            ]
        },
        "progress_state": {
            "str"   : "IN PROGRESS",
            "color" : "primary",
            "transition" :[
                "open_state",
                "wait_state",
                "done_state"
            ]
        },
        "wait_state" : {
            "str"   : "WAIT",
            "color" : "warning",
            "transition" :[
                "open_state",
                "progress_state",
                "done_state"
            ]
        },
        "done_state" : {
            "str"   : "DONE",
            "color" : "success",
            "transition" :[
                "open_state",
                "progress_state",
                "wait_state"
            ]
        }
    }

ALL_STATUS = [STATUS_LIST[status]['str'] for status in STATUS_LIST.keys()]

class Status():

    # Constructor
    def __init__(self,state:str = "OPEN"):
        # Input check
        input_error_flag = True
        exist_states = STATUS_LIST.keys()
        for exist_state in exist_states:
            exist_state_str = STATUS_LIST.get(exist_state)['str']
            if (exist_state_str == state):
                input_error_flag = False
                temp_state = exist_state

        if (input_error_flag):
            return None

        self.state       = temp_state
        self.state_str   = STATUS_LIST.get(self.state)['str']
        self.state_color = STATUS_LIST.get(self.state)['color']
        self.transition  = []
        for next_state in STATUS_LIST.get(self.state)['transition']:
            self.transition.append(
                {
                    "str"  : STATUS_LIST.get(next_state)['str'],
                    "color": STATUS_LIST.get(next_state)['color']
                }
            )
    
    # Change state
    def change_state(self,next_state:str):

        for state_str in STATUS_LIST.keys():
            temp_state = STATUS_LIST.get(state_str)
            if (next_state == temp_state['str']):
                self.state       = state_str
                self.state_str   = STATUS_LIST.get(self.state)['str']
                self.state_color = STATUS_LIST.get(self.state)['color']
    
    # Update Task status
    def update_TaskStatus(self,step_status):
        # Count each status numbers
        step_status_list = []
        for status in step_status:
            step_status_list.append(status.state_str)
        
        # Rule
        if (step_status_list.count("IN PROGRESS") > 0):
            self.change_state("IN PROGRESS")
        else:
            if (step_status_list.count("WAIT") > 0):
                self.change_state("WAIT")
            else:
                if (step_status_list.count("OPEN") == len(step_status_list)):
                    self.change_state("OPEN")
                elif (step_status_list.count("DONE") == len(step_status_list)):
                    self.change_state("DONE")
                else:
                    self.change_state("IN PROGRESS")
