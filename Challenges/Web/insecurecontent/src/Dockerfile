FROM zenika/alpine-chrome:with-puppeteer


COPY ./requirements.txt /app/requirements.txt
# switch working directory
WORKDIR /app

USER root

# Install python
RUN apk update
RUN apk add --no-cache python3 py3-pip

RUN python --version
RUN pip --version

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt --break-system-packages


# copy every content from the local file to the image
COPY . /app

RUN npm ci



# run
CMD ["python3", "app.py"]