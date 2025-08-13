import sys
import os

# Add the project root to Python path so tests can import chat_app
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root) 