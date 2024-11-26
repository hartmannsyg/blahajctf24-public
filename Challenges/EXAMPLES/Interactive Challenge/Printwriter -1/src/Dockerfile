FROM ubuntu

COPY ./main.py /srv/app/run
COPY ./flag.txt /srv/app/flag.txt

RUN chmod +x /srv/app/run

RUN apt-get update && apt-get install -y socat && apt-get install -y python2.7

RUN addgroup --gid 1001 nonroot && \
    adduser --uid 1001 --gid 1001 --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
USER 1001

WORKDIR /srv/app

CMD [ "socat", "TCP-LISTEN:8000,nodelay,reuseaddr,fork", "EXEC:\"timeout -s KILL 10m python2.7 -u /srv/app/run\"" ]