- Always use venv for Python projects

## Setup for Global Execution

To make the script executable from anywhere on your system, follow these steps:

### For `zsh` Users

**Make the Script Executable**

First, ensure your script is executable by adding the shebang line at the top of your script (`invoice.py`):

```python
#!/usr/bin/env python3
```
Then, change the permission to make it executable:

```sh
chmod +x /path/to/your/script/invoice.py
```
Replace /path/to/your/script/ with the actual directory path where your script resides.

Add Script Directory to PATH

Open your .zshrc file in a text editor:

```sh
nano ~/.zshrc
```
Append the following line to add your script's directory to the PATH environment variable:

```sh
export PATH="$PATH:/path/to/your/script/directory"
```
Remember to replace /path/to/your/script/directory with the actual path to the directory containing your script.

Save the file and apply the changes:

```sh
source ~/.zshrc
```

### Testing the Script
To verify that your script is set up correctly:

Open a new terminal window or tab to refresh your environment variables.

Run your script by its name:

```sh
./invoice.py
```
If you've set everything up correctly, you should be able to run your script and see the expected output or behavior.

### Troubleshooting
If you encounter a "Permission denied" error, make sure the script is set as executable:

```sh
chmod +x /path/to/your/script/invoice.py
```
If the system cannot find the command, ensure the script's directory is properly added to your PATH and that you've restarted your terminal or sourced your profile configuration file.


Feel free to adjust the snippet according to your project's specific requirements or directory structure.