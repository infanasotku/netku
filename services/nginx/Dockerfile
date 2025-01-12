FROM nginx:stable-alpine

ADD nginx.conf /etc/nginx/conf.d/default.conf
ADD install.sh /etc/install.sh

ARG DOMAIN
ARG AUTH_ADDR
ARG USER_ADDR
ARG KONG_ADDR
ARG XRAY_FALLBACK_PORT

RUN /etc/install.sh

CMD ["nginx", "-g", "daemon off;"]
