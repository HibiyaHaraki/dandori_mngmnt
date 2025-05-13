set port_num=5000

xcopy ".\instance\dandori_mngmnt.db" "C:\dandori_mngmnt_backup\"

start python server.py %port_num%

timeout /t 2
start "" http://localhost:%port_num%