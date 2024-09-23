FROM python:3.9.20-slim

LABEL maintainer="Maher NAIJA <maher.naija@gmail.com>"

WORKDIR /app/

ADD requirements/dev.txt /app

RUN pip install  --no-cache-dir -r /app/dev.txt

ADD ./src /app/

ADD ./scripts/entrypoint.sh /app/

RUN chmod +x  /app/entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
