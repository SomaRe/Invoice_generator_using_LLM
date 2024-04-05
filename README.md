# Invoice Management System

I part time as tutor and I'm tired to maintain and work with different excel files for each student, This is a Python script that provides me an interface for managing student invoices and performing various operations on a SQLite database through terminal. It uses the OpenAI module (for Open Api compatible API) to handle natural language prompts and execute corresponding functions or queries, I'm not explicitly using function calling as many local models are not compatible instead I used `reponse_format: {"type" : "json_object"}`.

I could totally do all this without using Large Language Models (LLMs), but honestly, using them just makes life easier. It's nice to be able to type out whatever I'm thinking, in any way it comes out, and the LLM still gets it. It crafts the SQL queries for me and fetches the info I need. This way, I don't have to build a bunch of functions for every single action. It's a straightforward and smart shortcut for my tutoring admin work!

## Features
* ✅ Add a new student with a specified rate and subject.
* ✅ Add a new payment for an existing student.
* ✅ Custom sql queries to fetch data from the database.
* ✖️ Generate an invoice for a specific student.
* ✖️ Create a new table to track billing history.
* ✖️ Ask confirmation before running any query that isn't read-only.
* ✖️ Function to update the rate or subject for an existing student.
* ✖️ Function to delete a student from the database.
* ✖️ STT support (I will probably wait for good open assistant and maybe combine with it).

## Prerequisites

- Python >= 3.10
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment(if using IDE, it might automatically activate the virtual environment, so you can skip this step):

   - On Windows:
    
        ```bash
        venv\Scripts\activate
        ```


    - On Linux/macOS:
        
        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:
    
    ```bash
    pip install -r requirements.txt
    ```


## Usage

The aim here is to be able to access the script from the command line and provide a natural language prompt to execute the corresponding function. This is achieved by using a batch file on Windows or adding the script directory to the PATH on Linux/macOS.

### Windows
Create a Batch File (I have already created a batch file named `invoice.bat` in the root directory of the project, you can use that or create a new one)

Create a new text file with a name like invoice.bat in the same directory as your invoice_management.py script.
Open the invoice.bat file in a text editor and add the following content:
batch

```bash
@echo off

rem Activate the virtual environment
call venv\Scripts\activate.bat

rem Run the Python script with the provided message
python invoice.py "%~1"
```
**Add Script Directory to PATH**


1. Open the Start menu and search for "Environment Variables".
2. Click on "Edit the system environment variables".
3. Click the "Environment Variables" button.
4. Under "System Variables", find the "Path" variable, and click "Edit".
5. Click "New" and add the path to the directory containing your invoice_management.py script and the invoice.bat file.
6. Click "OK" to save the changes.


**Testing the Script**

Open a new Command Prompt window to refresh your environment variables.
Run your script by typing:

```bash
invoice <message>
```
Replace <message> with the desired prompt or command.


For example:

```bash
run_invoice "Add a new student named John with a rate of 50 and subject math"
```

If you've set everything up correctly, you should be able to run your script and see the expected output or behavior.

### Linux/macOS

**Make the Script Executable**

First, ensure your script is executable by adding the shebang line at the top of your script (`invoice_management.py`):

```python
#!/usr/bin/env python3
```

Then, change the permission to make it executable:

```bash
chmod +x /path/to/your/script/invoice.py
```

Replace `/path/to/your/script/` with the actual directory path where your script resides.

**Add Script Directory to PATH**

Open your `.zshrc` or `.bashrc` file in a text editor:

```bash
nano ~/.zshrc  # For zsh users
```
or
```bash
nano ~/.bashrc  # For bash users
```
Append the following line to add your script's directory to the PATH environment variable:

```bash
export PATH="$PATH:/path/to/your/script/directory"
```

Remember to replace `/path/to/your/script/directory` with the actual path to the directory containing your script.

Save the file and apply the changes:

```bash
source ~/.zshrc  # For zsh users
```
or
```bash
source ~/.bashrc  # For bash users
```

**Testing the Script**

To verify that your script is set up correctly:

1. Open a new terminal window or tab to refresh your environment variables.
2. Run your script by its name:

```bash
./invoice.py <message>
```

If you've set everything up correctly, you should be able to run your script and see the expected output or behavior.

# Troubleshooting
If you encounter a "Permission denied" error on Linux/macOS, make sure the script is set as executable:

```bash
chmod +x /path/to/your/script/invoice_management.py
```

If the system cannot find the command, ensure the script's directory is properly added to your PATH and that you've restarted your terminal or sourced your profile configuration file.

On Windows, if you encounter any issues, make sure the virtual environment is activated correctly, and the script directory is added to the PATH environment variable.