
FROM python:3.10-slim-buster

WORKDIR /project

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn --workers 1 --bind 0.0.0.0:5000 WeatherApp:app 

