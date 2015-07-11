__author__ = 'Vojda'

from bottle import run, get, post, put, delete, response, request, server_names, ServerAdapter
import sources.utils.db_utils as db_utils
import sources.utils.utils as utils
from bson.json_util import dumps, loads
from sources.utils.skeleton import User, Recipe
import hashlib, time


COOKIE_LIFE = 604800000


# Declaration of new class that inherits from ServerAdapter
# It's almost equal to the supported cherrypy class CherryPyServer
class MySSLCherryPy(ServerAdapter):
    def run(self, handler):
        from cherrypy import _cpwsgi_server
        server = _cpwsgi_server.wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)

        # If cert variable is has a valid path, SSL will be used
        # You can set it to None to disable SSL
        cert = '/var/tmp/server.pem' # certificate path
        server.ssl_certificate = cert
        server.ssl_private_key = cert
        try:
            server.start()
        finally:
            server.stop()

# Add our new MySSLCherryPy class to the supported servers
# under the key 'mysslcherrypy'
server_names['mysslcherrypy'] = MySSLCherryPy

# class SSLWebServer(ServerAdapter):
#     """
#     CherryPy web server with SSL support.
#     """
#
#     def run(self, handler):
#         """
#         Runs a CherryPy Server using the SSL certificate.
#         """
#         from cherrypy import wsgiserver
#         from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter
#
#         server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
#
#         server.ssl_adapter = pyOpenSSLAdapter(
#             certificate="cert.crt",
#             private_key="private.key",
#             certificate_chain="intermediate_cert.crt"
#         )
#
#         try:
#             server.start()
#         except:
#             server.stop()
#
# server_names['sslwebserver'] = SSLWebServer

class SSLWSGIRefServer(ServerAdapter):
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket (
         srv.socket,
         certfile='server.pem',  # path to certificate
         server_side=True)
        srv.serve_forever()

@get('/hello')
def hello():
    return "Hello World!"


@post('/login')
def login():
    body = loads(request._get_body_string().decode(utils.ENCODING))
    if db_utils.is_user_valid(body['username'], body['password']):
        hash_object = hashlib.sha512(bytes(body['username'], 'utf-8'))
        hex_dig = hash_object.hexdigest()
        expires = utils.get_current_time() + COOKIE_LIFE
        db_utils.add_cookie(hex_dig, expires, body['username'])
        response.set_cookie('Hash', hex_dig)
        response.set_cookie('Alive_Until', str(expires))
    else:
        response.status = 401


@get('/users')
def get_all_users():
    response.content_type = 'application/json'
    return dumps([p.__dict__ for p in db_utils.get_all_users()])


@post('/users')
def add_user():
    if utils.is_admin(request.get_cookie('Hash')):
        response.content_type = 'application/json'
        body = loads(request._get_body_string().decode(utils.ENCODING))
        return dumps(db_utils.add_user(body['username'], body['password'], body['admin']))
    response.status = 401


@put('/users')
def edit_user():
    body = loads(request._get_body_string().decode(utils.ENCODING))
    hash = request.get_cookie('Hash')
    if utils.is_admin(hash) or body['username'] == db_utils.get_cookie(hash)['user']:
        db_utils.edit_user(User(body['username'], body['password'], body['admin']))
    response.status = 401


@get('/recipes')
def get_recipes():
    response.content_type = 'application/json'
    search_criteria = request.get_header('filter')
    if search_criteria is None:
        return dumps([p.__dict__ for p in db_utils.get_all_recipes()])
    else:
        return dumps([p.__dict__ for p in db_utils.find_recipes(loads(search_criteria))])


@post('/recipes')
def add_recipe():
    response.content_type = 'application/json'
    body = loads(request._get_body_string().decode(utils.ENCODING))
    return dumps(db_utils.add_recipe(Recipe(body['name'], body['products'], body['description'])))


@delete('/recipes')
def delete_recipe():
    if utils.is_admin(request.get_cookie('Hash')):
        id = loads(request.query.get('id'))
        db_utils.delete_recipe(id)
    else:
        response.status = 401

run(host='localhost', port='8080', server='mysslcherrypy', debug=True)
# srv = SSLWSGIRefServer(host="0.0.0.0", port=8090)
# run(server=srv)