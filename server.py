import cherrypy
import os
import config
from lib import controller
cherrypy.log("The hostname %r does not have an app_root entry   start.")

# from jinja2 import Environment, FileSystemLoader
# env = Environment(loader=FileSystemLoader('templates'))

# class Root:
#     @cherrypy.expose
#     def index(self):
#         tmpl = env.get_template('index.html')
#         return tmpl.render(salutation='Hello', target='World')

# cherrypy.config.update({'server.socket_host': '127.0.0.1',
#                          'server.socket_port': 8080,
                        # })
cherrypy.config.update(config.config)

# cherrypy.tree.mount()
# cherrypy.engine.start()
# cherrypy.engine.block()
cherrypy.quickstart(controller.Root(),script_name='/',config=config.config)
# cherrypy.start()
