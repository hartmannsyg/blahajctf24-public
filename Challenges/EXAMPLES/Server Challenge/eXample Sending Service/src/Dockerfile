FROM zenika/alpine-chrome:with-puppeteer

RUN mkdir app
WORKDIR app
COPY . .
RUN npm ci
EXPOSE 8000
USER root
RUN addgroup --gid 1001 nonroot && \
    adduser --uid 1001 -G nonroot --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
USER 1001
CMD ["node","app.js"]