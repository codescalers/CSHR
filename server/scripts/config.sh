#!/bin/sh

CONFIG_DIR=server_dir/config
ENV_DIR=${CONFIG_DIR}/.env
DJANGO_SECRET_KEY=$(poetry run python3 -c 'from django.utils.crypto import get_random_string; print(get_random_string(50))')


exec |
	# Touch the .env file

	echo 'DJANGO_SECRET_KEY'=$DJANGO_SECRET_KEY > ${ENV_DIR}
	echo 'DJANGO_DEBUG'=$DJANGO_DEBUG >> ${ENV_DIR}
	echo 'EMAIL'=$EMAIL >> ${ENV_DIR}
	echo 'EMAIL_PASSWORD'=$EMAIL_PASSWORD >> ${ENV_DIR}
	echo 'EMAIL_HOST'=$EMAIL_HOST >> ${ENV_DIR}
	echo 'REDIS_HOST'=$REDIS_HOST >> ${ENV_DIR}
	echo 'DJANGO_SUPERUSER_EMAIL'=$DJANGO_SUPERUSER_EMAIL >> ${ENV_DIR}
	echo 'DJANGO_SUPERUSER_PASSWORD'=$DJANGO_SUPERUSER_PASSWORD >> ${ENV_DIR}
	echo 'SERVER_DOMAIN_NAME'=$SERVER_DOMAIN_NAME >> ${ENV_DIR}
	echo 'CLIENT_DOMAIN_NAME'=$CLIENT_DOMAIN_NAME >> ${ENV_DIR}
