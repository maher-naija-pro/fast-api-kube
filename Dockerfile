FROM python:3.9.20-slim

LABEL maintainer="Maher NAIJA <maher.naija@gmail.com>"

WORKDIR /app/

ADD requirements/dev.txt /app

RUN pip install  --no-cache-dir -r /app/dev.txt

ADD ./src /app/

EXPOSE 8000

CMD ["hypercorn", "main:app", "-b", "0.0.0.0:8000", "--reload"]