FROM nginx:stable-alpine

ADD nginx.conf.template /etc/nginx/conf.templates/default.conf
ADD nginx.conf /etc/nginx/conf.d/infanasotku.conf
ADD run.sh /etc/run.sh

CMD /etc/run.sh && nginx -g 'daemon off;'