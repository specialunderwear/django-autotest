import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
from django.core.management.base import BaseCommand
from os import chdir
from django.conf import settings
from subprocess import Popen, PIPE 
from os.path import split, dirname, join, abspath, isfile
import os.path
import re


CURRENT_PATH =  abspath(dirname(__file__))
AUTOTEST_PATH = abspath(join(CURRENT_PATH, '..'))

def absolute_path(path):

    return os.path.abspath(os.path.normpath(path))

ERROR_REGEX = re.compile(r"FAIL:|ERROR:")

class LoggingEventHandler(FileSystemEventHandler):


    def run_test_suite(self, app_name):

        chdir(settings.PROJECT_DIR)
        result = Popen(['./manage.py', 'autotestrunner', app_name], stdout=PIPE, stderr=PIPE, close_fds=True).communicate() 
        
        print "".join(result)
        
        title = ''
        content = []
        for line in result:
            split_lines = line.split('\n')
            for l in split_lines:
                if l.startswith('Ran'):
                    title = l
                if ERROR_REGEX.match(l):
                    content.append(l)
        
        if content:
            chdir(AUTOTEST_PATH)
            os.system('./notify.sh "{0}" "{1}" '.format(title, "\n".join(content)))
        

    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)
        if isfile(event.src_path):
            for app in settings.INSTALLED_APPS:
                if app in event.src_path:
                    self.run_test_suite(app)
                    break
    

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()
    help = 'Runs the test suite when a tests file is saved'
    args = '[appname ...]'

    requires_model_validation = False

    def handle(self, *args, **options):
        #handler = AutotestEventHandler()
        handler = LoggingEventHandler()

        app_path = absolute_path(settings.PROJECT_DIR)

        observer = Observer()
        observer.schedule(handler, path=app_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

