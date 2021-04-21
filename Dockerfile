FROM python:3.9.0

WORKDIR /

ADD . .

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "run:app"]