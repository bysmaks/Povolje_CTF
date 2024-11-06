# Use the official PHP image with Apache
FROM php:7.4-apache

# Copy the application files to the container
COPY ./src /var/www/html/

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Install necessary PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Set the working directory
WORKDIR /var/www/html/

# Expose port 80
EXPOSE 80