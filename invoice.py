#!/usr/bin/env python3

import os
import sqlite3
import argparse
import json
import datetime
from typing import Optional, Dict, Tuple, List
import logging
from dotenv import load_dotenv
import setup_database
from openai import OpenAI
import config

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# System messages
FUNCTION_DESCRIPTION_MESSAGE = '''
You are an AI assistant for an invoice management system. Your responses will be in JSON format.
You have access to the following functions:

- add_student(name: str, per_hour_rate: float, subject: str) -> dict:
  Adds a new student to the database.
  Returns a JSON object with the following structure, do not include comments in the response:
  {
      "function": "add_student",
      "args": {
          "name": "<student_name>",  # The name of the student
          "per_hour_rate": <rate>,  # The hourly rate for the student
          "subject": "<subject>"  # The subject of the student
      }
  }

- add_invoice_entry(student_name: str, num_hours: float, session_date: Optional[str], comments: Optional[str]) -> dict:
  Adds a new invoice entry for a student.
  Returns a JSON object with the following structure, do not include comments in the response:
  {
      "function": "add_invoice_entry",
      "args": {
          "student_name": "<student_name>",  # The name of the student
          "num_hours": <hours>,  # The number of hours for the invoice entry
          "session_date": "<date>",  # The date of the session, set it to NULL if not specified (optional)
          "comments": "<comments>"  # Comments for the invoice entry, keep it empty if nothing specific is told. (optional)
      }
  }

- generate_invoice(student_name: str) -> dict:
    Generates an invoice for a student based on the invoice entries.
    Returns a JSON object with the following structure, do not include comments in the response:
    {
        "function": "generate_invoice",
        "args": {
            "student_name": "<student_name>"  # The name of the student
        }
    }
'''

SQL_QUERY_MESSAGE = '''
You are an AI assistant with knowledge of the following database schema:

Tables:
- students:
    - id: INTEGER (PRIMARY KEY)
    - name: TEXT (UNIQUE NOT NULL) # lowercase only
    - per_hour_rate: REAL (NOT NULL)
    - subject: TEXT (NOT NULL) # lowercase only
    - created_at: TIMESTAMP (DEFAULT CURRENT_TIMESTAMP)

- invoice_entries:
    - id: INTEGER (PRIMARY KEY)
    - student_id: INTEGER (FOREIGN KEY students(id))
    - num_hours: REAL (NOT NULL)
    - subject: TEXT (NOT NULL) # from students table
    - session_date: DATE (DEFAULT CURRENT_DATE)
    - comments: TEXT
    - created_at: TIMESTAMP (DEFAULT CURRENT_TIMESTAMP)

- generated_invoices:
    - id: INTEGER (PRIMARY KEY)
    - student_id: INTEGER (FOREIGN KEY students(id))
    - subject: TEXT (NOT NULL) # from students table
    - num_hours: REAL (NOT NULL)
    - total_amount: REAL (NOT NULL)
    - start_date: DATE (NOT NULL)
    - end_date: DATE (NOT NULL)
    - created_at: TIMESTAMP (DEFAULT CURRENT_TIMESTAMP)

Please provide an SQL query based on the request: "{request}"

Always return in JSON format.
example:
{{"request": "Give me the names of all students.",
 "sql_query": "SELECT name FROM students;"}}
'''

RESULT_PRESENTATION_MESSAGE = "You are an AI assistant that takes a request and results (that are rated from database), and presents them to users in a concise manner."

def add_student(student_name: str, per_hour_rate: float, subject: str) -> None:
    """
    Add a new student to the database.

    Args:
        student_name (str): The name of the student.
        per_hour_rate (float): The hourly rate for the student.
        subject (str): The subject of the student.
    """
    with sqlite3.connect('student_invoices.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO students (name, per_hour_rate, subject) VALUES (?, ?, ?)', (student_name.lower(), per_hour_rate, subject.lower()))
            connection.commit()
            logging.info(f"Student added: {student_name}, Rate: {per_hour_rate}, Subject: {subject}")
        except Exception as e:
            logging.error(f"Error adding student: {e}")


def add_invoice_entry(student_name: str, num_hours: float, session_date: Optional[str] = None, comments: Optional[str] = None) -> None:
    """
    Add a new invoice entry for a student.

    Args:
        student_name (str): The name of the student.
        num_hours (float): The number of hours for the invoice entry.
        session_date (str, optional): The date of the session in ISO format (e.g., '2024-01-01'). Defaults to today's date.
        comments (str, optional): Comments for the invoice entry. Defaults to None.
    """
    if session_date is None:
        session_date = datetime.date.today().isoformat()

    with sqlite3.connect('student_invoices.db') as connection:
        cursor = connection.cursor()
        try:
            # Fetch all students that match the given name pattern
            cursor.execute('SELECT id, name, subject FROM students WHERE name LIKE ?', (f'%{student_name}%',))
            matching_students = cursor.fetchall()

            if len(matching_students) > 1:
                print(f"More than one match found for '{student_name}':")
                for index, (student_id, student_name, subject) in enumerate(matching_students, start=1):
                    print(f"{index}) {student_name}")
                choice = int(input("Choose (enter the number): ")) - 1  # Adjust for zero-based index
                if choice < 0 or choice >= len(matching_students):
                    logging.error("Invalid choice. Exiting.")
                    return
                student_id, _, subject = matching_students[choice]
            elif len(matching_students) == 0:
                logging.error(f"No students found with the name '{student_name}'.")
                return
            else:
                student_id, _, subject = matching_students[0]

            # Insert the invoice entry with the chosen student's ID and subject
            cursor.execute('INSERT INTO invoice_entries (student_id, num_hours, subject, session_date, comments) VALUES (?, ?, ?, ?, ?)', (student_id, num_hours, subject, session_date, comments or ""))
            connection.commit()
            logging.info(f"Invoice entry added: {student_name}, Hours: {num_hours}, Date: {session_date}, Comments: {comments or 'None'}")
        except Exception as e:
            logging.error(f"Error adding invoice entry: {e}")


def generate_invoice(student_name: str) -> None:
    """
    Generate an invoice for a student based on the invoice entries.

    Args:
        student_name (str): The name of the student.
    """
    with sqlite3.connect('student_invoices.db') as connection:
        cursor = connection.cursor()
        try:
            # Fetch all students that match the given name pattern
            cursor.execute('SELECT id, name, per_hour_rate, subject FROM students WHERE name LIKE ?', (f'%{student_name}%',))
            matching_students = cursor.fetchall()

            if len(matching_students) > 1:
                print(f"More than one match found for '{student_name}':")
                for index, (student_id, student_name, per_hour_rate) in enumerate(matching_students, start=1):
                    print(f"{index}) {student_name}")
                choice = int(input("Choose (enter the number): ")) - 1  # Adjust for zero-based index
                if choice < 0 or choice >= len(matching_students):
                    logging.error("Invalid choice. Exiting.")
                    return
                student_id, _, per_hour_rate, subject = matching_students[choice]
            elif len(matching_students) == 0:
                logging.error(f"No students found with the name '{student_name}'.")
                return
            else:
                student_id, _, per_hour_rate, subject = matching_students[0]

            # Fetch all invoice entries for the student from generated_invoices last_date if available
            # first lets see if there is any invoice generated for this student
            cursor.execute('SELECT id, student_id, total_amount, start_date, end_date FROM generated_invoices WHERE student_id = ? ORDER BY end_date DESC LIMIT 1', (student_id,))
            last_invoice = cursor.fetchone()
            if last_invoice:
                last_invoice_id, _, _, last_end_date, _ = last_invoice
                cursor.execute('SELECT num_hours, session_date FROM invoice_entries WHERE student_id = ? AND session_date > ? ORDER BY session_date', (student_id, last_end_date))
            else:
                cursor.execute('SELECT num_hours, session_date FROM invoice_entries WHERE student_id = ? ORDER BY session_date', (student_id,))
            invoice_entries = cursor.fetchall()

            if not invoice_entries:
                logging.error(f"No invoice entries found for '{student_name}'.")
                return
            
            # Calculate the total amount for the invoice
            num_hours = sum(num_hours for num_hours, _ in invoice_entries)
            total_amount = num_hours * per_hour_rate

            # Insert the generated invoice into the database
            start_date = invoice_entries[0][1]
            end_date = invoice_entries[-1][1]
            cursor.execute('INSERT INTO generated_invoices (student_id, subject, num_hours, total_amount, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)', (student_id, subject, num_hours, total_amount, start_date, end_date))
            connection.commit()
            logging.info(f"Invoice generated for {student_name}: Hours: {num_hours}, Total Amount: {total_amount}, Start Date: {start_date}, End Date: {end_date}")

        except Exception as e:
            logging.error(f"Error generating invoice: {e}")


def get_response_from_llm(messages: List[Dict[str, str]], response_format: Optional[Dict[str, str]] = {"type": "json_object"}) -> Dict:
    """
    Send a request to the LLM and get the response.

    Args:
        messages (List[Dict[str, str]]): A list of dictionaries containing the messages to send to the LLM.
        response_format (Dict[str, str], optional): The format of the response to expect from the LLM. Defaults to None.

    Returns:
        Dict: The response from the LLM, either as a JSON object or as a string.
    """

    BASE_URL = os.getenv('BASE_URL', config.BASE_URL)
    API_KEY = os.getenv('API_KEY', config.API_KEY)
    MODEL = os.getenv('MODEL', config.MODEL)

    print(BASE_URL, API_KEY, MODEL)
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format=response_format,
        temperature=0.0,
    )

    logging.info(f"LLM Response: {response.choices[0].message.content}")
    if response_format is None:
        return response.choices[0].message.content
    return json.loads(response.choices[0].message.content)


def get_function_from_llm(prompt: str) -> Dict:
    """
    Get a function call from the LLM based on the provided prompt.

    Args:
        prompt (str): The prompt to send to the LLM.

    Returns:
        Dict: A dictionary containing the function name and arguments.
    """
    messages = [
        {'role': 'system', 'content': FUNCTION_DESCRIPTION_MESSAGE},
        {'role': 'user', 'content': prompt}
    ]

    return get_response_from_llm(messages, response_format={"type": "json_object"})


def execute_prompt(prompt: str) -> None:
    """
    Execute a prompt by getting a function call from the LLM and calling the corresponding function.

    Args:
        prompt (str): The prompt to send to the LLM.
    """
    function_call = get_function_from_llm(prompt)

    function_name = function_call["function"]
    args = function_call["args"]

    if function_name == "add_student":
        add_student(args["name"], args["per_hour_rate"], args["subject"])
    elif function_name == "add_invoice_entry":
        add_invoice_entry(args["student_name"], args["num_hours"], args.get("session_date"), args.get("comments"))
    elif function_name == "generate_invoice":
        generate_invoice(args["student_name"])


def handle_custom_request(request: str) -> None:
    """
    Handle a custom request by getting an SQL query from the LLM, executing it, and presenting the results.

    Args:
        request (str): The custom request to handle.
    """
    messages = [
        {'role': 'system', 'content': SQL_QUERY_MESSAGE.format(request=request)},
        {'role': 'user', 'content': request}
    ]

    query_info = get_response_from_llm(messages)
    if "sql_query" in query_info:
        results = execute_custom_sql(query_info["sql_query"])
        result_message = f"Request: {request}\nResults: {results}"
        messages = [
            {'role': 'system', 'content': RESULT_PRESENTATION_MESSAGE},
            {'role': 'user', 'content': result_message},
        ]
        get_response_from_llm(messages, response_format=None)
    else:
        logging.error("No SQL query provided by LLM.")


def execute_custom_sql(sql_query: str) -> str:
    """
    Execute a custom SQL query on the database.

    Args:
        sql_query (str): The SQL query to execute.

    Returns:
        str: A JSON string representing the query results.
    """
    with sqlite3.connect('student_invoices.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            logging.info(f"Custom SQL query executed: {results}")
            return json.dumps(results)
        except Exception as e:
            logging.error(f"Error executing custom SQL query: {e}")
            return "Error executing custom SQL query"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoice Management System")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("prompt", type=str, nargs='?', help="prompt to process")
    group.add_argument("-r", "--request", type=str, help="Custom request to process")

    args = parser.parse_args()
    
    setup_database.create_database_tables()

    if args.request:
        handle_custom_request(args.request)
    elif args.prompt:
        execute_prompt(args.prompt)
    else:
        logging.error("No prompt or request provided. Exiting.")
