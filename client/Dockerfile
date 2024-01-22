# build stage
FROM node:18.18.2 as build-stage
WORKDIR /app

ENV CSHR_API=$CSHR_API

COPY ./package*.json ./
RUN npm i -g pnpm
COPY client/ .
RUN pnpm install
RUN chmod +x /app/scripts/build-env.sh
RUN pnpm build

# production stage
FROM nginx:stable-alpine as production-stage
COPY ./nginx/prod.conf /temp/prod.conf

# Use the environment variable in the configuration file
RUN envsubst '$CSHR_API' < /temp/prod.conf > /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/scripts/build-env.sh /usr/share/nginx/html

EXPOSE 80

CMD ["/bin/sh", "-c", "/usr/share/nginx/html/build-env.sh && nginx -g \"daemon off;\""]
