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

The application is vulnerable to SQL injection. For example in `views.py`, in the function `post` the SQL statement is formed with a simple f-string substitution.

Example:

When making a post, enter the following as the title (single quotes included):

`' || (SELECT password FROM Users WHERE name = 'admin') || '`

This creates a post with the admin's password in the title. Very secure.

### A3:2017 - Sensitive Data Exposure

The application uses unencrypted HTTP messages to pass data – including password. This exposes the data to malicious actors. Below is a snippet from Wireshark's capture from logging in as admin:

```
csrfmiddlewaretoken=eqoUiIzpvuVz4FFFmtNuvtBsQuxakxIEo0nRXPO32ay12kostE59VTQvfTPCa1wF&username=admin&passwo
rd=coffee^@8^D^@^@^
```

Note the "coffee" in there - the default admin password is visible to anyone capturing the packet.

### A5:2017 - Broken Access Control

The application has weak access control. For example, going to `/user/1` shows any posts made by the user with id 1. However, this page also displays any posts marked as private (which are supposed to be viewable by only the user themselves), even without logging in.

### A7:2017 - Cross-Site Scripting

The application doesn't attempt to sanitize any data entered by users. For example, when making a post, enter the following as the image url:

`/logout`

This causes everyone to be logged out when refreshing the main page. You could also enter strings such as 

`\" onClick=alert("hacked!")`

which enable malicious JavaScript to be executed (in this case, it requires users to click the image, though)

Additionally, the URL provided could lead to an image with malicious data in it – SVG's, for example, can contain almost anything in them and should *not* be run from untrusted sources.

### A10:2017 - Insufficient Logging & Monitoring

The application does not do *any* logging or monitoring. Because of this, it could be very hard to notice any malicious activity, or even accidental errors, which enables the malfunctionality to continue uninterrupted.
