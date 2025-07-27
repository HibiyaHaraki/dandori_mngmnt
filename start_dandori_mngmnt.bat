
REM Set the port number for the server
set port_num=5000

REM Start the Python server on the specified port
start python server.py %port_num%

REM Wait for 2 seconds to allow the server to start
timeout /t 2

REM Open the default web browser to the local server URL
start "" http://localhost:%port_num%