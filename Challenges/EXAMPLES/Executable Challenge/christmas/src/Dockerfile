FROM ubuntu:22.04

COPY ./flag.txt /srv/app/flag.txt
ADD ./santa /srv/app/run

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run

RUN apt-get update && apt-get install -y socat

RUN addgroup --gid 1001 nonroot && \
    adduser --uid 1001 --gid 1001 --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
USER 1001

WORKDIR /srv/app

CMD [ "socat", "TCP-LISTEN:8000,nodelay,reuseaddr,fork", "EXEC:\"timeout -s KILL 10m /srv/app/run\"" ]
