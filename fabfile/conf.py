import datetime
from fabric.api import env


env.use_ssh_config = True
env.forward_agent = True
env.user = 'moment'
env.roledefs = {
    'web': ['212.71.251.102']
}

KEY = env.user

MACHINE = {
    'LOCATION': env.roledefs['web'][0],
    'PORT': 80,
    'NAME': 'Moment',
    'OWNER_GROUP': 'www-data',
    'OWNER_USER': env.user,
    'OWNER_PROFILE': '/home/' + env.user + '/.profile',
    'DIR_USER_HOME': '/home/' + env.user,
    'DIR_MODE': 'g+s',
    'DIR_WORKSPACE': '/srv',
    'DIR_ENVIRONMENTS': '/srv/environments',
    'DIR_PROJECTS': '/srv/projects',
    'DIR_SSL': '/srv/ssl',
    'DIR_LOGS': '/srv/logs',
    'DATABASES': ['redis'],
    'KEY': KEY,
    'ACTION_DATE': datetime.datetime.now()
}

PROJECT = {
    'APP_LOCATION': '127.0.0.1',
    'APP_PORT': 9000,
    'APP_WORKERS': 4,
    'APP_TIMEOUT': 30,
    'APP_WSGI': 'moment:app',
    'NAME': MACHINE['NAME'],
    'DOMAINS': ['moment.prjts.com'],
    'REPO': 'https://github.com/pwalsh/moment',
    'BRANCH': 'master',
    'ROOT': MACHINE['DIR_PROJECTS'] + '/' + KEY,
    'ENV': MACHINE['DIR_ENVIRONMENTS'] + '/' + KEY,
    'LOGS': {
        'NGINX_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_nginx_access.log',
        'NGINX_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_nginx_error.log',
        'GUNICORN_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_gunicorn_access.log',
        'GUNICORN_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_gunicorn_error.log',
        'REDIS_ACCESS': MACHINE['DIR_LOGS'] + '/' + KEY + '_redis_access.log',
        'REDIS_ERROR': MACHINE['DIR_LOGS'] + '/' + KEY + '_redis_error.log',
    },
    'KEY': KEY,
    'ACTION_DATE': datetime.datetime.now()
}
