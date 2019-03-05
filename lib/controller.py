import cherrypy
import datetime
import os,yaml,csv,sys
from pathlib import Path
import subprocess
import time
import sqlite3
import config
import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
print ("config path LIB {}"+format(config.path))
# Global variabels #
SESSION_KEY = '_cp_username'
samel_dir = 'sampel'
scriptDIR = 'ScriptPath'
scriptLogs= 'ScriptLogs'
yml_directory = 'YML'
scriptPath = 'BatchCode'
yaml_configFile = 'application.yaml'
dashbord_yml = 'Dashbord'
#sampel_dir_path = path+systempath+yml_directory+systempath+samel_dir
yml_dir_path = os.path.join(config.path,yml_directory,dashbord_yml)
#cherrypy.log("Application YAML path yml_dir_path [%s]"str(yml_dir_path))
cherrypy.log("Application YAML path " + yml_dir_path)


ScriptPath = os.path.join(config.path,scriptPath,scriptDIR)
cherrypy.log("Script path [%s]" % format(ScriptPath))


ScriptLogsdir = os.path.join(config.path,scriptPath,scriptLogs)
cherrypy.log("Script Logs path [%s]" % format(ScriptLogsdir))
session_path = os.path.join(config.path,'sessions')
cherrypy.log("session path [%s]" % format(session_path))
class Root:

	user = None
	Ymlform = None
	authentication = None
	script = None
	showlogs =None
	showremark =None

	def __init__(self):
		# self.user = User()
		self.script  = Script()
		self.ymlform  = Ymlform()
		self.showlogs =ShowLogs()
		self.authentication =authentication()
		self.showremark =ShowRemark()

	@cherrypy.expose
	def index(self):
		cherrypy.log("Load application index page")
		tmpl = env.get_template('index.html')
		return tmpl.render(salutation='Hello', target='World')

	@cherrypy.expose
	def broken(self):
		raise RuntimeError('Pretend something has broken')

class authentication:

	def on_login(self, username):
		raise cherrypy.HTTPRedirect('/ymlform/yml_form',username)

	def on_logout(self, username):
		"""Called when user is logout."""
		#raise cherrypy.HTTPRedirect("/")
		tmpl = env.get_template('index.html')
		return tmpl.render(msg='User success full logout!')

	@cherrypy.expose
	def uservaliation(self,username=None, password=None):
		#pass
		if username is None or password is None:
			tmpl = env.get_template('index.html')
			return tmpl.render(msg='Username/Password Not Matched')
		  	#return cherrypy.tools.template._engine.get_template('page/login.html').render()

		error_msg = check_credentials(username, password)
		cherrypy.log("return [%s]" % format(error_msg))
		if error_msg:
			msg = error_msg
			#return cherrypy.tools.template._engine.get_template('page/login.html',error_msg).render()
			tmpl = env.get_template('index.html')
			return tmpl.render(msg=msg)
			#return Index.index(self,msg)
			#return self.get_loginform(username, error_msg, from_page)
		else:

			cherrypy.session[SESSION_KEY]  = cherrypy.request.login = username


			cherrypy.log("SESSION ID  [%s]" %format(cherrypy.session.id))

			cherrypy.log("SESSION ID  [%s]" % format(cherrypy.session[SESSION_KEY]))
			raise cherrypy.HTTPRedirect('/ymlform/yml_form')

	@cherrypy.expose
	def logout(self):

		username = cherrypy.session.get(SESSION_KEY, None)
		cherrypy.request.cookie.get('session_id',None)
		cherrypy.session[SESSION_KEY] = cherrypy.request.login = None
		cherrypy.session[SESSION_KEY] = None
		username = cherrypy.session.get(SESSION_KEY, None)
		cherrypy.log("Action trigger before logout[%s]" % format(username))
		if username:
			cherrypy.log("Action trigger after log out [%s]" % format(username))
			cherrypy.request.login = None
			#cherrypy.session.clear()
			cherrypy.session.delete()
			raise cherrypy.HTTPRedirect("/")
			#cherrypy.session.expire()
			#os.unlink(os.path.join(session_path,'session-'+cherrypy.session.id))
			#tmpl = env.get_template('index.html')
                        #return tmpl.render(msg='User success full logout!')	
		else:
			cherrypy.request.login = None
			#cherrypy.session.clear()
			cherrypy.session.delete()
			raise cherrypy.HTTPRedirect("/")
			#cherrypy.session.expire()
                        #os.unlink(os.path.join(session_path,'session-'+cherrypy.session.id))
			#tmpl = env.get_template('index.html')
			#return tmpl.render(msg='User success full logout!')



def getusercredentials(username,password):

	user_dict ={}
	yml_dir = os.path.join(yml_dir_path,yaml_configFile)
	try:
		with open(yml_dir, 'r') as ymlfiledata:
			str_data = ymlfiledata.read()

		datafile = yaml.load(str_data)
		for listdata in datafile['application']:
			#print (type(listdata['user']))
			user_dict.update(listdata['user'])
		#print (user_dict)
		#print user_dict[username]+"----"+"---"+password
		if user_dict[username]:
			#print user_dict[username]+"----"+"---"+password
			if user_dict[username] == password:
				return True
		else:
			return False
	except:
		return "Yaml File not exist"

def check_credentials(username, password):
	"""Verifies credentials for username and password.
	Returns None on success or a string describing the error on failure"""
	# Adapt to your needs
	status = getusercredentials(username, password)
	cherrypy.log("return status [%s]" % format(status))
	cherrypy.log("validation [%s] [%s]" %(username, 'XXXX'))
	if status is True:
		return None
	else:
		return u"Incorrect username or password."

class Ymlform(object):

	@cherrypy.expose
	def yml_form(self):
		#print ("USERDETAILS [%s]" % format(cherrypy.session[SESSION_KEY]))
		#if not  cherrypy.session.has_keys(SESSION_KEY):
		#	print ("Not Exist")
		#	msg =None
                #        tmpl = env.get_template('index.html')
		#	return tmpl.render(msg=msg)
		try:
			if cherrypy.session[SESSION_KEY] is not None:
				uname =cherrypy.session[SESSION_KEY]
			#cherrypy.session.release_lock(session_path+systempath+'sessions'+systempath+'session-'+cherrypy.session.id)
				page ={}
				Getuserappliat ={}
				yml_dir = os.path.join(yml_dir_path,yaml_configFile)
				try:
					with open(yml_dir, 'r') as ymlfiledata:
						str_data = ymlfiledata.read()

					datafile = yaml.load(str_data)
					for listdata in datafile['application']:
						if uname in listdata['user']:
							page[listdata['app_name']] =listdata
						else:
							continue
					tmpl = env.get_template('app/yml_form.html')
					return tmpl.render(application=page,username=uname)
				except:
					tmpl = env.get_template('index.html')
					return tmpl.render(msg='Application config file Missing')
				#return {'application': page}
			else:
				#return cherrypy.tools.template._engine.get_template('page/login.html').render()
				msg =None
				tmpl = env.get_template('index.html')
				return tmpl.render(msg=msg)
		except:
			msg =None
			tmpl = env.get_template('index.html')
			return tmpl.render(msg=msg)

class ShowLogs:

	@cherrypy.expose
	def viewlogs(self,myFile=None):
		try:
			if cherrypy.session[SESSION_KEY] is not None:
				selected_dashbord = os.path.join(yml_dir_path,yaml_configFile)
				scriptlogs = ''
				scriptlog_output = None
				try:
					with open(selected_dashbord, 'r') as ymlfiledata:
						str_data = ymlfiledata.read()
						#datafile = yaml.safe_load(ymlfiledata)
						datafile = yaml.load(str_data)
					for listdata in datafile['application']:
						if listdata['app_name'] == myFile:
							scriptlogs = listdata['logfile']
					scriptlog_output = readloges(scriptlogs)
					return scriptlog_output
				except:
					return "Application Configuration file Missing!"
		except:
			msg =None
			tmpl = env.get_template('index.html')
			return tmpl.render(msg=msg)	

def readloges(logfilename):
	logfilenamepath = os.path.join(ScriptLogsdir,logfilename)
	try:
		with open(logfilenamepath,'r') as f:
			return json.dumps({'logs':f.read()})
	except:
		cherrypy.log("FILE NOT FOUND")
		return json.dumps({'logs':"Log file Not Create by Application.!"})

class Script:

	@cherrypy.expose
	def runscript(self,myFile=None):
		#cherrypy.session['ts'] = time.time()
		cherrypy.log("Loge File Name [%s]" % format(myFile))
		selected_dashbord = os.path.join(yml_dir_path,yaml_configFile)
		script = ''
		script_output = None
		try:
			with open(selected_dashbord, 'r') as ymlfiledata:
				str_data = ymlfiledata.read()
				#datafile = yaml.safe_load(ymlfiledata)
				datafile = yaml.load(str_data)
			for listdata in datafile['application']:
				if listdata['app_name'] == myFile:
					script = listdata['scipt_name']
			script_output = runscript(script)
			return script_output
		except:
			return "Application script Not exist!"

def runscript(name):

	#cherrypy.session.release_lock(session_path+systempath+'sessions'+systempath+'session-'+cherrypy.session.id)
	scriptName = os.path.join(ScriptPath,name)
	if os.path.isfile(scriptName):
		cherrypy.log("SCRIPTNAME [%s]" % format(scriptName))
		try:
			#cmd  =['sudo']
			#comand = 'iptables -L'
			#p = subprocess.Popen(scriptName, stdout=subprocess.PIPE, shell=True)
			p = subprocess.Popen([scriptName],stdout=subprocess.PIPE)
			## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
			## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. ##
			## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
			## or None, if no data should be sent to the child.
			(output, err) = p.communicate() ## Wait for date to terminate. Get return returncode ##
			p_status = p.wait()
			#p = subprocess.run([scriptName],stdout=subprocess.PIPE)
			#(output, err) = p.communicate()
			#p_status= "testing"
			cherrypy.log("Command output :[%s] " % format( output))
			cherrypy.log("Command exit status/return code : [%s]"% format(p_status))
			#return json.dumps({'output': p_status})
			#cherrypy.log("ERROR [%s]" % format(err))
			#cherrypy.log("errorcode [%s]" % format(p.returncode))
			return output
		except IOError:
			cherrypy.log("Error:Execution Fail, may be file not exist! ")
			return "Error: Execution Fail, may be file not exist!"
	else:
		return "Application script Not exist!"
class ShowRemark:

	@cherrypy.expose
	def remark(self,appname=None):
		selected_dashbord = os.path.join(yml_dir_path,yaml_configFile)
		print (selected_dashbord)
		remarks = []
		script_output = None
		if os.path.isfile(selected_dashbord):
			cherrypy.log("SCRIPTNAME CONFIGURATION Files[%s]" % format(selected_dashbord))
			with open(selected_dashbord, 'r') as ymlfiledata:
				str_data = ymlfiledata.read()
	  			#datafile = yaml.safe_load(ymlfiledata)
				datafile = yaml.load(str_data)
				#print (datafile)
			for listdata in datafile['application']:
				if listdata['app_name'] == appname:
					remarks = listdata['remarks']
			#cherrypy.log(remarks)
			print (remarks)
			#print json.dumps({'remarks':remarks})
			#cherrypy.log(json.dumps(remarks)
	
			return json.dumps(remarks)
			#except:
			#	print (json.dumps("Application  Configuration File Missing!"))
			#	return json.dumps("Application  Configuration File Missing!")
		else:
			print (json.dumps("Application  Configuration File Missing!"))
			return json.dumps("Application  Configuration File Missing!")
