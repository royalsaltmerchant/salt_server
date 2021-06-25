FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common gcc

WORKDIR /

ADD . .

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "run:app"]