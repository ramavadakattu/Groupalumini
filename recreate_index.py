#!/usr/bin/env python

import os


removefiles = os.system('rm -rf /home/djangoprojects/alumclub/indexes/*.*')


recreate_index = os.system('/home/djangoprojects/alumclub/manage.py syncdb')

recreate_index2 = os.system('/home/djangoprojects/alumclub/manage.py migrate')


output = os.popen('ls /home/djangoprojects/alumclub/indexes/').read()

print output
