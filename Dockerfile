FROM inspectorio/python

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -U -r /tmp/requirements.txt

EXPOSE 80
EXPOSE 443

CMD ["/app/entrypoint.sh"]