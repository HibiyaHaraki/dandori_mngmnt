set port_num=5000
start python server.py %port_num%

timeout /t 2
start "" http://localhost:%port_num%