FROM inspectorio/python

ARG APP_USER=app
ARG APP_GRP=app
ARG APP_HOME=/app
ARG APP_SHELL=/bin/bash

ENV prometheus_multiproc_dir /tmp/prom_data

COPY sample_data/ /etc/nginx/

RUN mkdir /tmp/prom_data \
&& chown -R "${APP_USER}:${APP_GRP}" /tmp/prom_data \
&& pip install --no-cache-dir -U -r "${APP_HOME}/src/requirements.txt"

EXPOSE 80
EXPOSE 443
EXPOSE 5000

CMD ["/app/entrypoint.sh"]