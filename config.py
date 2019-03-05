import os
import cherrypy

path   = os.path.abspath(os.path.dirname(__file__))

print (path)
#print ("config path {}".format(path))
#print ("config path logs {}".format(os.path.join(path, 'logs', 'cherrypy.access.log')))
#print ("config path session {}".format(os.path.join(path, 'sessions')))


config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
    'engine.autoreload.on' : False,
    'tools.trailing_slash.on' : False,
    'tools.sessions.on': True,
    'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
    'tools.sessions.storage_path': os.path.join(path, 'sessions'),
    'tools.sessions.timeout': 10,
    'log.access_file': os.path.join(path, 'logs', 'cherrypy.access.log'),
    'log.error_file': os.path.join(path, 'logs', 'cherrypy.error.log')
  },
  '/resource' : {
    'tools.staticdir.on'  : True,
    'tools.staticdir.dir' : os.path.join(path, 'public', 'resource')
  },
  '/css': {
      'tools.staticdir.on': True,
      'tools.staticdir.dir' : os.path.join(path, 'public', 'resource/css')
  },
  '/javascript': {
    'tools.staticdir.on': True,
    'tools.staticdir.dir' : os.path.join(path, 'public', 'resource/js')
  },
  '/images': {
    'tools.staticdir.on': True,
    'tools.staticdir.dir' : os.path.join(path, 'public', 'resource/images')
  },
  '/fonts': {
    'tools.staticdir.on': True,
    'tools.staticdir.dir' : os.path.join(path, 'public', 'resource/fonts')
  },
  '/style': {
    'tools.staticdir.on': True,
    'tools.staticdir.dir' : os.path.join(path, 'public', 'resource/style')
  },
  '/webfonts': {
    'tools.staticdir.on': True,
    'tools.staticdir.dir' : os.path.join(path, 'public', 'resource/webfonts')
  }
}
