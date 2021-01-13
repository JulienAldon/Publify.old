FROM    node:12.2.0-alpine AS build
RUN     apk add git

WORKDIR /app/publify_front
COPY    front/package.json front/package-lock.json /app/publify_front/
RUN     npm install
COPY    front /app/publify_front
RUN     npm run build

# TODO: Django's collectstatic

FROM nginx:latest
COPY --from=build /app/publify_front /srv/www/aldon.info/publify_front

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx-config /etc/nginx