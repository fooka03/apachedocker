FROM ubuntu:16.04
RUN apt update
RUN apt dist-upgrade -y
RUN apt install -y apache2 libapache2-mod-wsgi curl vim wget net-tools ca-certificates python supervisor

RUN mkdir -p /usr/local/www/wsgi-scripts
RUN mkdir -p /usr/local/www/documents
COPY wsgi.conf /etc/apache2/sites-available/
RUN ln -s /etc/apache2/sites-available/wsgi.conf /etc/apache2/sites-enabled
RUN rm /etc/apache2/sites-enabled/000-default.conf
COPY fib.wsgi /usr/local/www/wsgi-scripts/

RUN mkdir -p /var/log/supervisor
COPY apache.conf /etc/supervisor/conf.d/apache.conf

CMD ["/usr/bin/supervisord"]
