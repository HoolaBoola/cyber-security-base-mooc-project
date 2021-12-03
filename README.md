# Super Secure Social Media Website

## Table Of Contents

- [Super Secure Social Media Website](#super-secure-social-media-website)
  * [Installation](#installation)
    + [Using the install script](#using-the-install-script)
    + [Installing manually](#installing-manually)
  * [Launching the program](#launching-the-program)
    + [Launch using the script](#launch-using-the-script)
    + [Launch manually](#launch-manually)
  * [Vulnerabilities - OWASP 2017](#vulnerabilities---owasp-2017)
    + [A1:2017 - Injection](#a1-2017---injection)
    + [A3:2017 - Sensitive Data Exposure](#a3-2017---sensitive-data-exposure)
    + [A5:2017 - Broken Access Control](#a5-2017---broken-access-control)
    + [A6:2017 - Security Misconfiguration](#a6-2017---security-misconfiguration)
    + [A7:2017 - Cross-Site Scripting](#a7-2017---cross-site-scripting)
    + [A10:2017 - Insufficient Logging & Monitoring](#a10-2017---insufficient-logging---monitoring)

<small><i>Table of contents generated with <a href='http://ecotrust-canada.github.io/markdown-toc/'>markdown-toc</a></i></small>


## Installation

The installation and launching of the server are more or less how other Django projects in the course are started. Regardless, below are explicit instructions on how to use the program.

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

## Vulnerabilities - OWASP 2017

### A1:2017 - Injection

The application is vulnerable to SQL injection. For example in [`views.py`](website/views.py), in the function `post` the SQL statement is formed with a simple f-string substitution.

Example:

When making a post, enter the following as the title (single quotes included):

`' || (SELECT password FROM Users WHERE name = 'admin') || '`

This creates a post with the admin's password in the title. Very secure.

**Steps to fix the issue**:

Use parametrized queries.

Instead of
```Python
stmt = f"INSERT INTO Posts (var1, var2, var3, ... ) VALUES ('{var1}', '{var2}', '{var3}', ...);"
cursor.execute(stmt)
```

use something like

```Python
stmt = "INSERT INTO Posts (var1, var2, var3, ... ) VALUES ( ?, ?, ?, ...);"
args = (var1, var2, var3, ...)
cursor.execute(stmt, args)
```

[Link to example](https://www.kite.com/python/answers/how-to-bind-variables-to-a-sql-query-in-sqlite3-in-python)

### A3:2017 - Sensitive Data Exposure

The application uses unencrypted HTTP messages to pass data – including password. This exposes the data to malicious actors. Below is a snippet from Wireshark's capture from logging in as admin:

```
csrfmiddlewaretoken=eqoUiIzpvuVz4FFFmtNuvtBsQuxakxIEo0nRXPO32ay12kostE59VTQvfTPCa1wF&username=admin&passwo
rd=coffee^@8^D^@^@^
```

Note the "coffee" in there - the default admin password is visible to anyone capturing the packet.

**Steps to fix the issue**:

Use greater encryption. Get an SSL Certificate and use that for more secure data transfer. For example, [this](https://simpleisbetterthancomplex.com/tutorial/2016/05/11/how-to-setup-ssl-certificate-on-nginx-for-django-application.html) guide shows how to do it with Django.

### A5:2017 - Broken Access Control

The application has weak access control. For example, going to `/user/1` shows any posts made by the user with id 1. However, this page also displays any posts marked as private (which are supposed to be viewable by only the user themselves), even without logging in.

This issue itself is not that severe, in that users should not be storing sensitive data on a website such as this, to begin with – even if it's supposed to be marked as "private". 

**Steps to fix the issue**:

In [`views.py`](website/views.py), in every function (in this case, `posts_by_user`), make sure to verify that the user has the correct session key before displaying any data that should not be displayed. Depending on the specification, the correct behaviour could be to display all posts made by the user *except* for the ones marked private, or not show any posts to other users.

### A6:2017 - Security Misconfiguration

The program does not have a dedicated, generic error page to which it would redirect users. Instead, it often displays Django's error messages with complete stack traces, exposing the server's inner workings to attackers.

Example: go to `/post` and click `Post` without first logging in.

**Steps to fix the issue**:

In every function, make sure the user is logged in first. This could be done using Django's `@login_required` (which, for "security" purposes, was not done in this project), or by using the same method used in `index`:

```Python
if not request.session.get("username"):
    return redirect("/login")
```

Additionally, a generic error page should be created where Django would redirect users, instead of the overly-specific one used currently.

### A7:2017 - Cross-Site Scripting

The application doesn't attempt to sanitize any data entered by users. For example, when making a post, enter the following as the image url:

`/logout`

This causes everyone to be logged out when refreshing the main page. You could also enter strings such as 

`\" onClick=alert("hacked!")`

which enable malicious JavaScript to be executed (in this case, it requires users to click the image, though)

Additionally, the URL provided could lead to an image with malicious data in it – SVG's, for example, can contain almost anything in them and should *not* be run from untrusted sources.

**Steps to fix the issue**:

Sanitize any HTML written by the user. Make sure the user input is actually a valid URL, and make sure the URL actually points to an image, and not to a location such as `/logout`. 

Make sure the image is valid (and doesn't have malicious code embedded in it). This can be tricky, but could be done for example with ImageMagick. 

Only accept images from trusted websites, for example image hosting services such as imgur.com.

Sanitize user input where appropriate. For example, using `urllib`, the above example with JavaScript would result in 

```Python
  urllib.parse.quote('\" onClick=alert("hacked!")')
> '%22%20onClick%3Dalert%28%22hacked%21%22%29'
```

OWASP's [XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) is also a good resource. 

### A10:2017 - Insufficient Logging & Monitoring

The application does not do *any* logging or monitoring. Because of this, it could be very hard to notice any malicious activity, or even accidental errors, which enables the malfunctionality to continue uninterrupted.

**Steps to fix the issue**:

There is no single way to fix the issue, as it's just too broad and there could always be something that was forgotten to log. 

However, there are multiple ways to make the situation much better.

Every time a user logs in, fails to log in or produces an error, the event should be logged with enough information, in a proper format. Python's `logging` [library](https://docs.python.org/3/library/logging.html#logrecord-attributes) is a good example with sensible defaults. Django's documentation has good [guides](https://docs.djangoproject.com/en/3.2/topics/logging/) as well.
