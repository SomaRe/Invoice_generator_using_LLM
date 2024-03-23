# Invoice Management System

This is a Python script that provides an interface for managing student invoices and performing various operations on a SQLite database. It uses the OpenAI API to handle natural language prompts and execute corresponding functions.

## Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

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

### Linux/macOS

**Make the Script Executable**

First, ensure your script is executable by adding the shebang line at the top of your script (`invoice_management.py`):

```python
#!/usr/bin/env python3
Then, change the permission to make it executable:
```

```bash
chmod +x /path/to/your/script/invoice_management.py
```

Replace /path/to/your/script/ with the actual directory path where your script resides.

**Add Script Directory to PATH**

Open your .zshrc or .bashrc file in a text editor:

```bash
nano ~/.zshrc  # For zsh users
nano ~/.bashrc  # For bash users
```
Append the following line to add your script's directory to the PATH environment variable:

```bash
export PATH="$PATH:/path/to/your/script/directory"
```

Remember to replace /path/to/your/script/directory with the actual path to the directory containing your script.

Save the file and apply the changes:

```bash
source ~/.zshrc  # For zsh users
source ~/.bashrc  # For bash users
```

**Testing the Script**

To verify that your script is set up correctly:

1. Open a new terminal window or tab to refresh your environment variables.
2. Run your script by its name:

```bash
./invoice.py
```

If you've set everything up correctly, you should be able to run your script and see the expected output or behavior.

### Windows
Create a Batch File

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

Troubleshooting
If you encounter a "Permission denied" error on Linux/macOS, make sure the script is set as executable:

```bash
chmod +x /path/to/your/script/invoice_management.py
```

If the system cannot find the command, ensure the script's directory is properly added to your PATH and that you've restarted your terminal or sourced your profile configuration file.

On Windows, if you encounter any issues, make sure the virtual environment is activated correctly, and the script directory is added to the PATH environment variable.