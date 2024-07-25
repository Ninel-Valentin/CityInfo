FROM python

ENV REDIS_HOST=redis-weather

ADD . /Services/RedisWeather
WORKDIR /Services/RedisWeather

RUN pip install -r requirements.txt

EXPOSE 5002
CMD [ "python", "app.py" ]