# Django RPyC App

#### RPyC Documentation: <a href="https://rpyc.readthedocs.io/en/latest/"> https://rpyc.readthedocs.io/en/latest/ </a>

Extends the capabalities of RPyC to a Django Application.

## Requisites

1) RPyC
2) Django
3) Django-Bootstrap3
4) Pandas

<pre>
pip install rpyc
pip install django
pip install django-bootstrap3
pip install pandas
</pre>

Some linux system may require 
<pre>
apt-get install django-admin
</pre>

Both the master and slave must have RPyC installed in them.
rpyc_classic.py in /usr/local/bin directory or in the Scripts directory in your Python installation directory.

A set of small tasks can be predefined which will get executed on the target machine on a click.
Users can also upload script files where arguments are taken as sys arguments to the application and can execute the script on a single click from the Django application on the slave service machine.

Web client can connect to the target machine without any authentication process as RPyC takes care of it. The security game can be anted up by using key files whose path can be supplied as an argument while executing daemon process. Forms by default have an CSRF token embedded making it secure from web scrapers or bots.


The application is cross-platform compliant. By default it throws an error page when a .bat file is tried to be executed on a POSIX system and the vice versa for .sh files on Windows environments.

A csv file is maintained which will tell the application the number and labels of parameters required for the script file which the admin will fill out at the time of uploading the file. The same csv will be updated automatically when the admin uploads a new script file into the repo.

Basically this application invokes the shell of the target machine and executes commands or runs files through it. The scope of this application extends the scope of the shell of the platform of the target machine.

Exceptions are handled with suitable try-except statements throughout which will let the user know precise information about the error during the runtime.

#### All operations can be logged by saving the output of the daemon process to a file.

## Can be implemented for automating L1, L2 ticket solving in the infrastructure domain. 
