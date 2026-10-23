FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

ARG AIRFLOW_HOME=/opt/airflow
ARG AIRFLOW_UID=1000
ARG AIRFLOW_GID=0

WORKDIR ${AIRFLOW_HOME}
RUN mkdir -p dags logs plugins
COPY airflow.cfg .
COPY requirements.txt .
COPY entrypoint.sh .

RUN useradd -ms /bin/bash -u ${AIRFLOW_UID} -g ${AIRFLOW_GID} airflow
RUN chown -v -R "${AIRFLOW_UID}:${AIRFLOW_GID}" ${AIRFLOW_HOME}

RUN pip install "apache-airflow==3.1.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.1.1/constraints-3.10.txt"
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
