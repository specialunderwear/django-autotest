=================
django-autotest
=================

Django autotest is a custom command for your applications
that runs the test suite when you save a test file and displays
a desktop notification with the results.

===============
 Installation
===============


1. Install the package with ``pip install django_autotest`` or alternatively you can  
download the tarball and run ``python setup.py install``

2. Add ``autotest`` to your INSTALLED_APPS list in settings.py
   

::

	INSTALLED_APPS = ('autotest')



3. Add a PROJECT_DIR variable to ``settings.py`` with the absolute path to your Django application. 

::

	from os.path import abspath, dirname 

	PROJECT_DIR = abspath(dirname(__file__))
	
	# or if you have already defined that for another purposes ( templates for example )
	PROJECT_DIR = MY_PROJECT_DIR_DIRECTORY


=========
 Usage 
=========

::

    ./manage.py autotest



==================
 Additional notes
==================



===============
 Requirements
===============


Django 1.2+

watchdog

For the notifications:

libnotify ( Linux )
Growl ( Windows and Mac )


