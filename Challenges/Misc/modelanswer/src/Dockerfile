# start by pulling the python image
FROM python:3.11-slim-bookworm

RUN apt update && apt install -y socat

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

RUN adduser --uid 1001 --disabled-password nonroot
USER 1001

ENTRYPOINT ["sh"]
CMD [ "/app/entry.sh" ]