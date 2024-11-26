FROM debian:12

COPY ./chal /srv/app/run
COPY ./entry.sh /srv/app/entry.sh
RUN chmod 555 /srv/app/run
RUN chmod 555 /srv/app/entry.sh
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get install -y socat libc6:i386 libstdc++6:i386

RUN addgroup --gid 1001 nonroot && \
    adduser --uid 1001 --gid 1001 --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
USER 1001

WORKDIR /srv/app

CMD [ "/srv/app/entry.sh" ]