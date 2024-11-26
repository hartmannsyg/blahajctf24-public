# start by pulling the python image
FROM python:3.12-slim

RUN apt update && apt install -y socat

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install numpy

# copy every content from the local file to the image
COPY . /app

ENTRYPOINT ["sh"]
CMD [ "/app/entry.sh" ]