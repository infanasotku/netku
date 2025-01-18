FROM nginx:stable-alpine

ADD ./gateways/nginx/nginx.conf /etc/nginx/conf.d/default.conf
ADD ./gateways/nginx/run.sh /etc/run.sh

CMD ["/etc/run.sh"]
