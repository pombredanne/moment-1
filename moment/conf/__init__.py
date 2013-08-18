import os


CONF_ROOT = os.path.abspath(os.path.dirname(__file__))

APP_ROOT = os.path.abspath(os.path.dirname(CONF_ROOT))

WORK_ROOT = os.path.abspath(os.path.dirname(APP_ROOT))

TEMPLATE_ROOT = os.path.join(APP_ROOT, 'templates')

STATIC_ROOT = os.path.join(WORK_ROOT, 'static')

CAPTURES_ROOT = os.path.join(STATIC_ROOT, 'captures')

STATIC_URL = '/static/'

REDIS = {
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'DB': 0,
}

REDIS_URL = 'redis://' + REDIS['HOST'] + ':' + unicode(REDIS['PORT']) + '/' + \
            unicode(REDIS['DB'])

REDIS_KEY_PREFIX = 'moment,'

PHANTOM = '/usr/local/bin/phantomjs'

CASPER = '/usr/local/bin/casperjs'

CAPTURE_SCRIPT = os.path.join(APP_ROOT, 'capture.js')


# if we are on production, we should have a conf.production module to load.
# conf.production is generated via fabric for production environments.
try:
    from moment.conf.production import *
except ImportError:
    # if we are on local, we accept overrides in a conf.local module.
    # For safety, we only try to load conf.local if conf.production
    # does not exist.
    try:
        from moment.conf.local import *
    except ImportError:
        pass
