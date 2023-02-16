FROM python:3.10

WORKDIR /app

COPY . . 
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get -y install cron vim
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
# CMD /etc/init.d/cron start && tail -f /var/log/cron.log
# CMD ["cron", "-f"]