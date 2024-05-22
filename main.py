import os
import subprocess


# Directory paths of child directories
child_directories = ["Movies_scrapper", "Hockey_team", "Advance_forms"]

# Paths of Python scripts within child directories
script_paths = ["main.py", "main.py", "main.py"]
# Path to the virtual environment Python interpreter
venv_python = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python")  # Assuming venv is the name of the virtual environment directory

# Loop through each child directory and execute the corresponding script
for directory, script in zip(child_directories, script_paths):
    # Change working directory to the child directory
    os.chdir(os.path.join(os.getcwd(), directory))
    
    # Execute the Python script using the virtual environment Python interpreter
    subprocess.run([venv_python, script])
    
    # Move back to the parent directory
    os.chdir(os.path.join(os.getcwd(), ".."))