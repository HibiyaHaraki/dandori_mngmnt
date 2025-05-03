#
# May 2025. Created by Hibiya Haraki
#
# server.py
#

import os
from dandori_mngmnt import app, db

if __name__ == '__main__':
    if (not os.path.isfile('dandori_mngmnt/instance/dandori_mngmnt.db')):
        with app.app_context():
            db.create_all()
    app.run()