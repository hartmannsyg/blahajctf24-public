# start by pulling the python image
FROM python:3.12-slim

RUN apt update

# switch working directory
WORKDIR /app

# copy every content from the local file to the image
COPY . /app

ENTRYPOINT ["sh"]
CMD [ "/app/entry.sh" ]