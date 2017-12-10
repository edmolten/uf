FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install cron
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
ARG PORT
ENV PORT=${PORT}
ADD crontab /etc/cron.d/uf-cron
RUN chmod 0644 /etc/cron.d/uf-cron
RUN touch /var/log/cron.log
CMD bash start.sh