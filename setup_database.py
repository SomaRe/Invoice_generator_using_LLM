import sqlite3
import logging

# Configure logging (if this is your main script or if you want specific configurations for this script)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

def create_database_tables():
    connection = sqlite3.connect('student_invoices.db')
    cursor = connection.cursor()

    try:
        # Check if students table exists and create if not
        if not check_table_exists(cursor, "students"):
            cursor.execute('''
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    per_hour_rate REAL NOT NULL,
                    subject TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            logging.info("Students table created.")

        # Check if invoice_entries table exists and create if not
        if not check_table_exists(cursor, "invoice_entries"):
            cursor.execute('''
                CREATE TABLE invoice_entries (
                    id INTEGER PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    num_hours REAL NOT NULL,
                    subject TEXT NOT NULL,
                    session_date DATE DEFAULT CURRENT_DATE,
                    comments TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id)
                )
            ''')
            logging.info("Invoice entries table created.")

        # Check if generated_invoices table exists and create if not
        if not check_table_exists(cursor, "generated_invoices"):
            cursor.execute('''
                CREATE TABLE generated_invoices (
                    id INTEGER PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    subject TEXT NOT NULL,
                    num_hours REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id)
                )
            ''')
            logging.info("Generated invoices table created.")

        connection.commit()
    except Exception as e:
        logging.error(f"Error setting up database: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    create_database_tables()
