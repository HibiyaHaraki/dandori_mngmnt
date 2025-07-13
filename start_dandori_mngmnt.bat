set port_num=5000
python server.py %port_num%
pause
rem timeout /t 2
rem start "" http://localhost:%port_num%