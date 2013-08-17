from flask import Flask
from redis import StrictRedis
from rq import Queue
from moment import conf


app = Flask(__name__, template_folder=conf.TEMPLATE_ROOT,
            static_folder=conf.STATIC_ROOT)

app.config.from_object(conf)

redis = StrictRedis(host=conf.REDIS['HOST'], port=conf.REDIS['PORT'],
                    db=conf.REDIS['DB'])

q = Queue(connection=redis)


import moment.views
import moment.models
