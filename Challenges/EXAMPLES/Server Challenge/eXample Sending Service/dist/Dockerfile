FROM zenika/alpine-chrome:with-puppeteer

RUN mkdir app
WORKDIR app
COPY . .
RUN npm ci

EXPOSE 3000
CMD ["node","app.js"]