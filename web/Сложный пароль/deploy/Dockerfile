FROM php:8.2-fpm
RUN apt-get update && apt-get install -y \
		libfreetype-dev \
		libjpeg62-turbo-dev \
		libpng-dev \
	&& docker-php-ext-configure gd --with-freetype --with-jpeg \
	&& docker-php-ext-install -j$(nproc) gd

RUN apt install nginx -y
RUN apt install gettext-base -y


COPY ./default.conf /etc/nginx/conf.d/default.conf.template 
COPY ./www.conf /usr/local/etc/php-fpm.d/www.conf
EXPOSE 9000

COPY ./app /var/www/html
COPY ./entrypoint.sh /etc/entrypoint.sh
RUN chmod +x /etc/entrypoint.sh

ENTRYPOINT ["/etc/entrypoint.sh"]