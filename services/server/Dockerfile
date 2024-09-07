FROM nginx:stable-alpine

ADD nginx.conf.template /etc/nginx/conf.templates/default.conf
ADD nginx.conf /etc/nginx/conf.d/infanasotku.conf
ADD install.sh /etc/install.sh

ARG PORT
ARG DOMAIN
ENV PORT $PORT
ENV DOMAIN $DOMAIN

RUN /etc/install.sh

CMD ["nginx", "-g", "daemon off;"]