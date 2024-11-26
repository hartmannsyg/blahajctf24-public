FROM php:8.2-apache
COPY src/ /var/www/html/
#COPY src/000-default.conf /etc/apache2/000-default.conf
COPY src/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY src/ports.conf /etc/apache2/ports.conf
RUN mkdir /var/www/html/databases
RUN chmod 777 /var/www/html/databases
EXPOSE 8000
CMD ["apache2-foreground"]