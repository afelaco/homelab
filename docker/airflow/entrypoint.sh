#!/bin/bash
set -e

if [ "$1" = "scheduler" ]; then
    airflow db migrate
    airflow users create \
        --username "${_AIRFLOW_WWW_USER_USERNAME}" \
        --password "${_AIRFLOW_WWW_USER_PASSWORD}" \
        --firstname Airflow \
        --lastname Admin \
        --role Admin \
        --email admin@example.com
fi

exec airflow "$@"
