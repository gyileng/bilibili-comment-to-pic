#!/usr/bin/env bash

PYTHON_BIN="$HOME/anaconda3/envs/code-gy/bin/python"
GUNICORN_BIN="/$HOME/anaconda3/envs/code-gy/bin/gunicorn"
PROJECT_PATH="$HOME/code-gy"
PYTHON_PATH="${PROJECT_PATH}/orange-box"
PID_FILE="${PROJECT_PATH}/pid/orange-box.pid"
ACCESS_LOG="${PROJECT_PATH}/log/orange-box/gunicorn_access.log"
ERROR_LOG="${PROJECT_PATH}/log/orange-box/gunicorn_error.log"

BIND="0.0.0.0:8888"
WORK_CLASS="gevent"
WORKS=3
GRACEFUL_TIMEOUT=1

APP="apps:app"
COMMAND="--bind ${BIND} \
        --worker-class ${WORK_CLASS} \
        --workers ${WORKS} \
        --pythonpath ${PYTHON_PATH} \
        --pid ${PID_FILE} \
        --graceful-timeout ${GRACEFUL_TIMEOUT} \
        --access-logfile ${ACCESS_LOG} \
        --error-logfile ${ERROR_LOG} \
        --capture-output \
        --daemon"

case "$@" in
    start)
        if [ -f "$PID_FILE" ]; then
            kill -TERM $(cat ${PID_FILE})
            sleep ${GRACEFUL_TIMEOUT}
        fi
        ${GUNICORN_BIN} ${COMMAND} ${APP}
    ;;
    stop)
        kill -TERM $(cat ${PID_FILE})
    ;;
    quit)
        kill -QUIT $(cat ${PID_FILE})
    ;;
    restart)
        if [ -f "$PID_FILE" ]; then
            kill -TERM $(cat ${PID_FILE})
            sleep ${GRACEFUL_TIMEOUT}
        fi
        ${GUNICORN_BIN} ${COMMAND} ${APP}
    ;;
    reload)
        kill -HUP $(cat ${PID_FILE})
    ;;
    status)
        if [ ! -f "$PID_FILE" ]; then
            echo "PID:" "no pid"
        else
            echo "PID": $(cat ${PID_FILE})
        fi
    ;;
    statistic)
        SETTINGS=${PROJECT_PATH}/config/admin_server/settings.py
        ${PYTHON_BIN} ${PYTHON_PATH}/statistic.py
    ;;
    *)
        echo 'unknown arguments args(start|stop|quit|restart|reload|status)'
        exit 1
    ;;
esac