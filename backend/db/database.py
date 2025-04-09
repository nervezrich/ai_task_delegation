import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


# Define file paths
TASKS_CSV = os.path.join("data", "tasks.csv")
USERS_CSV = os.path.join("data", "task_history.csv")
DATA_FOLDER = ""

def load_csv(file_path):
    """ Load CSV data into Pandas DataFrame """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None
    
def save_csv(df, filename):
    """Save a pandas DataFrame to a CSV file (overwrite existing)."""
    filepath = os.path.join(DATA_FOLDER, filename)
    df.to_csv(filepath, index=False)
