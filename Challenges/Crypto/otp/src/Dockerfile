# start by pulling the python image
FROM python:3.8-alpine

RUN apk update && apk add socat

COPY ./chal.py /srv/app/run.py
COPY ./entry.sh /srv/app/entry.sh
RUN chmod 555 /srv/app/run.py
RUN chmod 555 /srv/app/entry.sh

RUN adduser --uid 1001 --disabled-password nonroot
USER 1001

WORKDIR /srv/app

CMD [ "/srv/app/entry.sh" ]