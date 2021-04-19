FROM python:3.9.0

WORKDIR /

ADD . .

RUN pip3 install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]