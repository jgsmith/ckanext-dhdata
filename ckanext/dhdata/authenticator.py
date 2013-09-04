from repoze.who.interfaces import (IChallenger, IIdentifier, IAuthenticator)
from webob import Request
from paste.request import get_cookies
from paste.auth import auth_tkt
from pylons import request

from webob.exc import HTTPFound
from zope.interface import implements

from paste.request import parse_dict_querystring
from paste.request import construct_url

from logging import getLogger

import ckan.model as model

import ckan.plugins as p

log = getLogger(__name__)

class FormPluginBase(object):
    def _get_rememberer(self, environ):
        rememberer = environ['repoze.who.plugins'][self.rememberer_name]
        return rememberer

    # IIdentifier
    def remember(self, environ, identity):
        rememberer = self._get_rememberer(environ)
        return rememberer.remember(environ, identity)

    #IIdentifier
    def forget(self, environ, identity):
        rememberer = self._get_rememberer(environ)
        return rememberer.forget(environ, identity)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, id(self))

class DrupalLogin(FormPluginBase):

    implements(IChallenger, 
               IIdentifier, 
               IAuthenticator)

    def __init__(self, path_logout, path_login, path_logout_return, secret, rememberer_name):
        self.path_logout = path_logout
        self.path_login = path_login
        self.path_logout_return = path_logout_return
        self.ticket_secret = secret
        self.rememberer_name = rememberer_name
            
    def challenge(self, environ, status, app_headers, forget_headers):
        if environ.has_key('rwpc.logout'):
            log.debug("Headers before logout: " + str(app_headers))
            app_headers = [(a, b) for a, b in app_headers \
                           if a.lower() != 'location' ]
            log.debug("Headers after logout: " + str(app_headers))
            headers = [('Location', self.path_logout)]
            headers = headers + app_headers + forget_headers
            log.debug("Logout headers: " + str(headers))
            return HTTPFound(headers=headers)
        else:
            headers = [('Location', login_url)]
            cookies = [(h,v) for (h,v) in app_headers \
                       if h.lower() == 'set-cookie']
            headers = headers + forget_headers + cookies

            return HTTPFound(headers=headers)

    def identify(self, environ):
        if environ.has_key('rwpc.logout'):
            return

        uri = environ.get('REQUEST_URI', construct_url(environ))
        query = parse_dict_querystring(environ)

        cookies = get_cookies(environ) 
        cookie = cookies.get('auth_tkt') 


        if cookie is None or not cookie.value: 
            return None 
 
        remote_addr = '0.0.0.0' 

        identity = {}
         
        try: 
            timestamp, userid, tokens, user_data = auth_tkt.parse_ticket( 
                self.ticket_secret, cookie.value, remote_addr) 
        except auth_tkt.BadTicket as e: 
            return None 
        #userObj = model.Session.query(model.User).filter_by(id=userid).first()
        #if userObj is None:
        #    return None
        #identity['login'] = userObj.name
        identity['login'] = userid
        return identity

    def authenticate(self, environ, identity):
        return identity.get('login')

def make_plugin(path_logout='', path_login='', path_logout_return='', secret='', rememberer_name=''):
    required_keywords = ('path_login', 'path_logout', 'secret', 'rememberer_name')
    for kw in required_keywords:
        if not eval(kw):
            raise ValueError(
                'DHData authentication plugin configuration must include {}.'.format(kw))

    plugin = DrupalLogin(
        path_logout=path_logout,
        path_login=path_login,
        path_logout_return=path_logout_return,
        secret=secret,
        rememberer_name=rememberer_name)
    return plugin
