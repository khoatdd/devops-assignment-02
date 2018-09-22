FROM inspectorio/python

COPY requirements.txt /tmp/requirements.txt
COPY sample_data/devops-assignment.inspectorio.info.crt /etc/nginx/
COPY sample_data/devops-assignment.inspectorio.info.key /etc/nginx/

RUN pip install --no-cache-dir -U -r /tmp/requirements.txt

EXPOSE 80
EXPOSE 443

CMD ["/app/entrypoint.sh"]