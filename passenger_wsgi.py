import sys, os

# Passenger on cPanel runs the default python, which is python 2
# so the first thing we do is force a switch to python3 in the virtualenv

INTERP = "/home/uralholidays/venv/bin/python"

# sys.executable is the path of the running Python
# Check to see that the correct Python version is running. The first
# time this runs, it won't be! Second time round, it should be.
# First argument to os.execl is the program to execute (INTERP);
# the second argument is the first part of the arguments to it, which
# is the full path to the executable itself.
# sys.argv is the rest of the arguments originally passed to the INTERP program.

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

# The arguments to setdefault must match the configuration in the main() function in your manage.py file

environ=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_app.settings')

# Import the app variable from your Django project wsgi file

from booking_app.wsgi import application
