
"""
config.py
Configuration file for Flask and SQLAlchemy settings in Dandori Management.

Created by Hibiya Haraki, May 2025.
"""

# Enable debug mode for development
DEBUG = True

# SQLite database URI for SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///dandori_mngmnt.db'

# Track modifications of objects (set to True for development, False for production)
SQLALCHEMY_TRACK_MODIFICATIONS = True