# start by pulling the python image
FROM python:3.11-slim-bookworm

# switch working directory
WORKDIR /app

# copy every content from the local file to the image
COPY . /app

RUN chmod 555 /app/enotes
RUN chmod 555 /app/libc.so.6
RUN chmod 555 /app/ld-linux-x86-64.so.2
RUN chmod 444 /app/flag.txt

RUN addgroup --gid 1001 nonroot && \
    adduser --uid 1001 --gid 1001 --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
USER 1001

RUN pip install psutil

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]
