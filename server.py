#
# May 2025. Created by Hibiya Haraki
#
# server.py
#

import os
import sys
from dandori_mngmnt import app, db

if __name__ == '__main__':
    # Get input port value
    port_num = 5000
    if (len(sys.argv) > 1):
        port_num = int(sys.argv[1])
        
    if (not os.path.isfile('dandori_mngmnt/instance/dandori_mngmnt.db')):
        with app.app_context():
            db.create_all()
    app.run(port=port_num)