# start by pulling the python image
FROM python:3.8-alpine

# switch working directory
WORKDIR /app

RUN apk update
RUN apk add firefox
RUN apk add font-terminus
COPY ./requirements.txt /app/requirements.txt
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app
RUN chmod 777 /app/screenshots
RUN adduser --uid 1001 --disabled-password nonroot
USER 1001
# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
