FROM python:3.9.20-slim

WORKDIR /app/
ADD requirements/dev.txt /app

RUN pip install -r /app/dev.txt

ADD . /app/

EXPOSE 8000

CMD ["hypercorn", "src/main:app", "-b", "0.0.0.0:8000", "--reload"]