# build stage
FROM node:18.18.2 as build-stage
WORKDIR /app

ENV SERVER_DOMAIN_NAME_API=$SERVER_DOMAIN_NAME_API

COPY ./client/package*.json ./
COPY ./docker/scripts/frontend/build-env.sh ./scripts
COPY client/ .

RUN npm i -g pnpm && pnpm install && pnpm build

# production stage
FROM nginx:stable-alpine as production-stage
COPY ./nginx/prod.conf /temp/prod.conf

# Use the environment variable in the configuration file
RUN envsubst '$SERVER_DOMAIN_NAME_API' < /temp/prod.conf > /etc/nginx/conf.d/default.conf
RUN chmod +x /app/scripts/build-env.sh

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/scripts/build-env.sh /usr/share/nginx/html

EXPOSE 80

CMD ["/bin/sh", "-c", "/usr/share/nginx/html/build-env.sh && nginx -g \"daemon off;\""]
