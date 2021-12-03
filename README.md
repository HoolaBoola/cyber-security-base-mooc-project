# Super Secure Social Media Website

The installation and launching of the server are more or less how other Django projects in the course are started. Regardless, below are explicit instructions on how to use the program.

## Installation

Clone this repository to your machine. You can install the project either with the provided script or doing it manually.

**Note**: the install script might not work in every case, in which case you should refer to the manual instructions.

### Using the install script 

Execute `install.sh` located in the root of this project.

### Installing manually

Ensure you have Python 3 installed.

In the project's root, execute the following to create a virtual environment: 

`python3 -m venv venv`

Enter the virtual environment with

`source venv/bin/activate`

If your shell is Fish, Csh or Powershell, call the corresponding file instead of `activate`. For example, in Fish you would call `source venv/bin/activate.fish`.

Now, with your virtual environment active, install the required dependencies with

`python3 -m pip install -r requirements.txt`

To exit the virtual environment, enter `deactivate`.

## Launching the program

You can launch the server with the provided script or do it manually.

**Note**: the launch script might not work in every case, in which case you should refer to the manual instructions.

### Launch using the script 

You can launch the server by executing `launch.sh`

### Launch manually

Make sure you're using the virtual environment (see above).

Create the database by running the `create_db.py` file:

`python3 create_db.py`

Now you can start the server with 

`python3 manage.py runserver`

You might receive error messages regarding "unapplied migrations". To fix this, stop the process and run 

`python3 manage.py migrate`

## OWASP 2017

### A1:2017 - Injection

### A3:2017 - Sensitive Data Exposure

### A5:2017 - Broken Access Control

### A7:2017 - Cross-Site Scripting

\" onClick=alert("hacked!")

### A10:2017 - Insufficient Logging & Monitoring

