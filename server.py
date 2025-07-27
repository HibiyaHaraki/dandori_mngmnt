
"""
server.py
Entry point for running the Dandori Management Flask application.

Created by Hibiya Haraki, May 2025.
"""

import os
import sys
from dandori_mngmnt import app, db

if __name__ == '__main__':
    # Get input port value from command line argument, default to 5000
    port_num = 5000
    if len(sys.argv) > 1:
        port_num = int(sys.argv[1])

    # Create database if it does not exist
    if not os.path.isfile('dandori_mngmnt/instance/dandori_mngmnt.db'):
        with app.app_context():
            db.create_all()

    # Run the Flask app
    app.run(port=port_num)