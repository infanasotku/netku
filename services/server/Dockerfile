FROM nginx:stable-alpine

ADD nginx.conf /etc/nginx/conf.d/nginx.conf
ADD install.sh /etc/install.sh
ADD run.sh /etc/run.sh

ARG ASSISTANT_PORT
ARG DOMAIN
ARG XRAY_FALLBACK_PORT
ENV ASSISTANT_PORT $ASSISTANT_PORT
ENV DOMAIN $DOMAIN
ENV XRAY_FALLBACK_PORT $XRAY_FALLBACK_PORT

RUN /etc/install.sh

CMD ["/bin/sh", "/etc/run.sh"]
