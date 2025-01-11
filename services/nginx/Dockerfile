FROM nginx:stable-alpine

ADD nginx.conf /etc/nginx/conf.d/nginx.conf
ADD install.sh /etc/install.sh
ADD run.sh /etc/run.sh

ARG DOMAIN
ARG AUTH_ADDR
ARG API_GATEWAY_ADDR
ARG XRAY_FALLBACK_PORT
ENV DOMAIN $DOMAIN
ENV AUTH_ADDR $AUTH_ADDR
ENV API_GATEWAY_ADDR $API_GATEWAY_ADDR
ENV XRAY_FALLBACK_PORT $XRAY_FALLBACK_PORT

RUN /etc/install.sh

CMD ["nginx", "-g", "daemon off;"]
# CMD ["/bin/sh", "/etc/run.sh"]
