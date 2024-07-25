# FROM ubuntu

# RUN apt-get update
# RUN apt-get install -y python3 python-is-python3

FROM python

ENV DB_HOST=172.17.0.2
ENV DB_NAME=cityinfo
ENV DB_PORT=3306
ENV DB_USER=dbadmin
ENV DB_PASS=dbadmin-pass

# Will be overwritten
ENV EVENT_SERVICE_URL=0.0.0.0
ENV WEATHER_SERVICE_URL=0.0.0.0

ADD . /Services/Gateway
WORKDIR /Services/Gateway

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app_gateway.py"] # asta este procesul care ruleaza cand qcreez containerul
