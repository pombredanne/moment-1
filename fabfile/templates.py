hosts = """### Generated via Fabric on ${ACTION_DATE}
# hosts configuration for ${NAME}
${LOCATION} ${KEY}
"""


profile = """### Generated via Fabric on ${ACTION_DATE}
# .profile configuration for ${NAME}
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export EDITOR=nano
export PYTHONIOENCODING=utf-8
export WORKON_HOME=${DIR_ENVIRONMENTS}
export PROJECT_HOME=${DIR_PROJECTS}
source /usr/local/bin/virtualenvwrapper.sh
export PIP_VIRTUAL_ENV_BASE=$WORKON_HOME
"""


nginx = """### Generated via Fabric on ${ACTION_DATE}
# nginx configuration for ${NAME}

upstream ${KEY} {
    server    ${APP_LOCATION}:${APP_PORT};
}

server {
    listen      *:${PORT};
    server_name ${SERVER_NAMES};
    root                 ${PROJECT_ROOT};
    access_log           ${ACCESS_LOG};
    error_log            ${ERROR_LOG};

    location /static/ {

    }

    location / {
        proxy_pass              http://${KEY};
        proxy_redirect          off;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size    10m;
        client_body_buffer_size 128k;
        proxy_connect_timeout   90;
        proxy_send_timeout      90;
        proxy_read_timeout      90;
        proxy_buffers           32 4k;
    }
}
"""


gunicorn_supervisor = """; Generated via Fabric on ${ACTION_DATE}
; gunicorn configuration for ${NAME}
; usually would pass logs on gunicorn, but it errors:
; --access-logfile ${ACCESS_LOG} --error-logfile ${ERROR_LOG}

[program:${KEY}-gunicorn]

command=${PROJECT_ENV}/bin/gunicorn --bind ${APP_LOCATION}:${APP_PORT} --timeout ${APP_TIMEOUT} --workers ${APP_WORKERS} ${APP_WSGI}

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${KEY}
redirect_stderr=true
autostart=true
autorestart=true
"""


rq_supervisor = """### Generated via Fabric on ${ACTION_DATE}
# rq configuration for ${NAME}
[program:${KEY}-rq]

command=${PROJECT_ENV}/bin/rqworker

environment=PATH="${PROJECT_ENV}/bin"
directory=${PROJECT_ROOT}
user=${KEY}
redirect_stderr=true
autostart=true
autorestart=true
"""


production_settings = """### Generated via Fabric on ${ACTION_DATE}
from openbudget.settings.base import *


"""
