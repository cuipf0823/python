#!/bin/bash

export GM_SERVER_DEV_PORT=23000
export GM_SERVER_TEST_PORT=23000
export GM_SERVER_TEST_IP='10.0.1.202'
export SECRET_KEY='gm_tool'
export GM_SERVER_DEV_IP='10.0.1.202'
export GM_LOG_MODE=0

python manage.py runserver -h 10.0.1.202 &
exit 0