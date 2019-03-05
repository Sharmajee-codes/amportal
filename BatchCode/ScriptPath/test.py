import cherrypy
import datetime
import os,yaml,csv,sys
from pathlib import Path
import subprocess
import time
import sqlite3
#import config
import json


scriptName ='/home/appadmin/webapp/AMP/BatchCode/ScriptPath/crm_maintenance_test.sh'
p = subprocess.Popen(scriptName, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate() ## Wait for date to terminate. Get return returncode ##
p_status = p.wait()
#p_status= "testing"
print("Command output :[%s] " % format( output))
print("Command exit status/return code : [%s]"% format(p_status))
