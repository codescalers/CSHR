#!/bin/sh

if [ -d dist ] 
then
    file="dist/config.js"
else
    file="config.js"
fi

if [ -z "$SERVER_API_URL" ] || [ -z "$SERVER_BASE_URL" ]; then
        echo "Error: Missing required env vars! Server intgration skipped."
        # exit 1
else
    configs="
        window.configs = {
            SERVER_API_URL: '$SERVER_API_URL',
            SERVER_BASE_URL: '$SERVER_BASE_URL',
        };
    "
fi


if [ -e $file ]
then
    rm $file
fi

echo $configs > $file