FROM node:12 AS build

WORKDIR /client

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
COPY package.json ./
# COPY yarn.lock ./
RUN apt-get update && apt-get install -y openssh-server nginx && npm install
COPY . ./
RUN npm run build
RUN chmod +x /client/start.sh
FROM nginx:1.19-alpine
COPY --from=build /app/public /usr/share/nginx/html