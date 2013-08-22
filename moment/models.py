import os
import logging
import subprocess
import json
import hashlib
from moment import redis, conf, utilities


USER_KEY_PREFIX = conf.REDIS_KEY_PREFIX + 'user,'

CAPTURE_KEY_PREFIX = conf.REDIS_KEY_PREFIX + 'capture,'


class Model(object):
    """Exposes the common structure of our data models."""

    prefix = None

    fields = (('', ''),)

    def __init__(self, request_params=None, **kwargs):

        self.fields_as_dict = dict(self.fields)
        self.kwargs = kwargs
        self.request_params = request_params
        self.arguments = self._normalize_kwargs()

    def put(self, *args, **kwargs):

        raise NotImplementedError

    def delete(self, *args, **kwargs):

        raise NotImplementedError

    def _normalize_kwargs(self):

        """Normalize all keyword arguments for a standardized interface.

        Our Model objects take arbitrary keyword arguments. These are passed in
        from Flask's request.args, and **kwargs.

        We then prune the passed arguments according to our Model's declared
        fields, by doing the following:

        * Remove any keyword arguments that are not in self.field_names
        * Ensure that all fields in self.field_names are represented with
        default values if they were not passed in via request.args or **kwargs

        The output of our normalization is self.arguments

        """

        arguments = {}

        if self.kwargs:

            arguments.update(
                {k: self.kwargs[k] for k in self.fields_as_dict if k in self.kwargs})

        if self.request_params:

            arguments.update(
                {k: self.request_params.get(k) for k in self.fields_as_dict})

        for k in self.fields_as_dict:

            if not k in arguments or not arguments[k]:

                arguments[k] = self.fields_as_dict[k]

        return arguments


class User(Model):
    """Methods for working with user data."""

    prefix = USER_KEY_PREFIX

    fields = (
        ('username', ''),
        ('secret', ''),
        ('token', ''),
    )

    def put(self):
        """Create or update a user."""

        if not 'key' in self.arguments or not self.arguments['key']:

            if not 'username' in self.arguments or not self.arguments['username']:

                raise ValueError('Creating a new user requires a username.')

            key = self.prefix + utilities.generate_uuid()

            username = self.arguments['username']

            token = self._token(key, username)

            secret = self._secret(key, username)

            redis.hset(key, 'username', username)

            redis.hset(key, 'secret', secret)

            redis.hset(key, 'token', token)

        else:

            key = self.arguments['key']

            update_values = self.arguments.copy()

            del update_values['key']

            for k, v in update_values:
                redis.hset(key, k, v)

            token = redis.hget(key, 'token')

        return key, token

    def is_valid(self):
        """Will return truthy or falsy on either key or token"""

        key = self.prefix + self.request_params['user']

        validity = redis.hget(key, 'token')

        return validity

    def _secret(self, key, username):

        secret = hashlib.md5(key + username).hexdigest()

        return secret

    def _token(self, key, username):

        token = hashlib.md5(self._secret(key, username) + username).hexdigest()

        return token


class Capture(Model):
    """Methods for working with capture data."""

    prefix = CAPTURE_KEY_PREFIX

    fields = (
        ('user', ''),  # 'uuid' segment of user key
        ('url', ''),  # 'http://www.example.com/'
        ('target', 'body'),  # '#content' or 'body' or '.account-widget'
        ('format', 'png'),  # 'pdf' or 'png' or 'jpg' or 'gif'
        ('viewport', '1280,800'),  # '1280,800' or '1280' or 'viewport_keyword'
        ('full', 'true'),  # 'true' or 'false'. false clips to viewport height.
        ('thumb', ''),  # 'width,height,position' or 'width,height,x,y'
        ('crop', ''),  # 'width,height,position' or 'width,height,x,y'
        ('unique', ''),  # 'any_unique_string' [e.g.] '2013-03-28T11:27:48.571Z'
        ('delay', '300'),  # 'int' [e.g.] '300' - wait for capture
        ('quality', '100'),  # 'int'
        ('events', ''),  # 'event,selector[,delay]' or 'event,x,y[,delay]' - chain with '+'
        ('renderer', 'webkit')  # 'webkit' or 'gecko'
    )

    viewport_keywords = [
        {'iphone4-portrait' : '320,480'},
        {'iphone4-landscape': '480,320'},
        {'tablet-portrait'  : '768,1024'},
        {'tablet-landscape' : '1024,768'},
        {'macbook-pro'      : '1280,800'}
    ]

    engine = 'phantomjs'

    engine_loglevel = 'debug'

    def put(self, image):
        """Create a capture object."""

        key = self.get_key()

        obj = redis.set(key, image)

        if obj:

            return key

    def get_key(self):
        """Get or create a key for this capture."""

        if 'key' in self.arguments:

            return self.arguments['key']

        key = self.prefix + hashlib.md5(
            json.dumps(self.arguments, sort_keys=True)).hexdigest()

        return key

    def capture(self):
        """Make a capture according to the passed arguments.

        Doing some extra logging here to help with later analysis of any probs
        that might come from the subprocess.

        """

        filename = '{key}.{format}'.format(key=self.get_key().lstrip(self.prefix),
                                           format=self.arguments['format'])

        image = os.path.join(conf.CAPTURES_ROOT, filename)

        if self.arguments['renderer'] == 'gecko':

            self.engine = 'slimerjs'

        params = [conf.CASPER,
                  '--log-level={level}'.format(level=self.engine_loglevel),
                  '--engine={engine}'.format(engine=self.engine),
                  conf.CAPTURE_SCRIPT,
                  image,
                  self.arguments['url'],
                  self.arguments['viewport'],
                  self.arguments['target'],
                  self.arguments['full'],
                  self.arguments['crop'],
                  self.arguments['delay'],
                  self.arguments['events'],
                  self.arguments['quality'],
                  self.arguments['thumb'],
        ]

        casper = subprocess.Popen(params, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        casper_output, casper_errors = casper.communicate()

        logging.info(casper_output)
        logging.info(casper_errors)
        logging.info(casper.returncode)

        # Here we are relying on convention:
        # If success, subprocess.returncode == 0
        # This could be fragile, need to investigate.
        if casper.returncode:

            raise Exception(casper_errors)

        else:

            return image


def q_capture_put(image=None, **kwargs):
    """Wraps the capture.put() method for later execution on a q."""

    capture = Capture(**kwargs)

    capture.put(image)

    return capture.get_key()


def create_user(**kwargs):
    """Creates a new user."""

    user = User(**kwargs)

    key = user.put()

    return key
