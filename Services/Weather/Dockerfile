# FROM ubuntu

# RUN apt-get update
# RUN apt-get install -y python3 python-is-python3

FROM python

ENV DB_HOST=172.17.0.2
ENV DB_NAME=cityinfo
ENV DB_PORT=3306
ENV DB_USER=dbadmin
ENV DB_PASS=dbadmin-pass

ADD . /Services/Weather
WORKDIR /Services/Weather

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app_weather.py"] # asta este procesul care ruleaza cand qcreez containerul
